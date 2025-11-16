import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import hashlib, uuid

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import models
from models import Patient, Appointment, Report, HumanTask
db.init_app(app)

with app.app_context():
    db.create_all()

# ---- Utilities ----
def generate_id(prefix='id'):
    return f"{prefix}_" + uuid.uuid4().hex[:8]

def mock_check_doctor_availability(doctor='Dr. Sharma', dt=None):
    # Mock: doctor is busy on even hours; free otherwise
    if dt is None:
        dt = datetime.utcnow() + timedelta(days=1)
    return dt.hour % 2 == 1

def call_llm_generate_confirmation(patient_name, doctor, dt):
    # Placeholder for LLM call - for now returns a templated message.
    return f"Hi {patient_name}, your appointment with {doctor} is confirmed for {dt.strftime('%d %b %Y %I:%M %p')}. Please upload any lab reports here."

# ---- Webhook (simulate WhatsApp) ----
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json or {}
    text = data.get('text','').strip()
    phone = data.get('from','unknown')
    # Simple intent rules
    if 'appointment' in text.lower() or 'book' in text.lower():
        # Extract simple info (mock)
        patient_name = data.get('name') or 'Patient'
        doctor = data.get('doctor') or 'Dr. Sharma'
        # prefer requested datetime or next available
        requested = data.get('datetime')
        dt = None
        if requested:
            try:
                dt = datetime.fromisoformat(requested)
            except:
                dt = datetime.utcnow() + timedelta(days=1)
        else:
            dt = datetime.utcnow() + timedelta(days=1, hours=15)
        available = mock_check_doctor_availability(doctor, dt)
        if not available:
            # find next slot (add 1 hour until free)
            attempts = 0
            while not available and attempts < 12:
                dt = dt + timedelta(hours=1)
                available = mock_check_doctor_availability(doctor, dt)
                attempts += 1
        # Save appointment tentatively
        appt = Appointment(id=generate_id('appt'), patient_name=patient_name, patient_phone=phone, doctor=doctor, scheduled_for=dt, status='tentative', created_at=datetime.utcnow())
        db.session.add(appt)
        db.session.commit()
        # Create human review task if time within 24 hours (business rule)
        if dt - datetime.utcnow() < timedelta(hours=24):
            task = HumanTask(id=generate_id('task'), appointment_id=appt.id, task_type='confirm_soon', created_at=datetime.utcnow(), status='open')
            db.session.add(task)
            db.session.commit()
            resp = call_llm_generate_confirmation(patient_name, doctor, dt) + "\nNote: A staff member will confirm within 2 hours."
        else:
            resp = call_llm_generate_confirmation(patient_name, doctor, dt)
        return jsonify({'message': resp, 'appointment_id': appt.id})
    elif 'upload report' in text.lower() or 'report' in text.lower():
        # instruct user to upload via /upload-report
        return jsonify({'message': 'Please upload your lab report file at /upload-report (multipart form). Include appointment_id or phone.'})
    else:
        return jsonify({'message': 'Sorry, I did not understand. You can say "Book appointment" or "Upload report".'})

# ---- File upload endpoint (report) ----
@app.route('/upload-report', methods=['POST'])
def upload_report():
    # accept file and appointment_id or phone
    appt_id = request.form.get('appointment_id')
    phone = request.form.get('phone')
    f = request.files.get('file')
    if not f:
        return jsonify({'error':'No file uploaded'}), 400
    filename = f.filename
    save_path = os.path.join('uploads', filename)
    os.makedirs('uploads', exist_ok=True)
    f.save(save_path)
    # find appointment/patient
    appt = None
    if appt_id:
        appt = Appointment.query.filter_by(id=appt_id).first()
    elif phone:
        appt = Appointment.query.filter_by(patient_phone=phone).order_by(Appointment.created_at.desc()).first()
    # create report entry
    report = Report(id=generate_id('rpt'), appointment_id=appt.id if appt else None, filename=save_path, uploaded_at=datetime.utcnow(), status='processing')
    db.session.add(report)
    db.session.commit()
    # Create human review task for OCR verification
    task = HumanTask(id=generate_id('task'), report_id=report.id, task_type='verify_report_ocr', created_at=datetime.utcnow(), status='open')
    db.session.add(task)
    db.session.commit()
    return jsonify({'message':'Report received. Our team will process and summarize it shortly.', 'report_id': report.id})

# ---- Admin dashboard ----
@app.route('/admin')
def admin_index():
    appts = Appointment.query.order_by(Appointment.created_at.desc()).limit(30).all()
    tasks = HumanTask.query.filter_by(status='open').order_by(HumanTask.created_at.asc()).all()
    reports = Report.query.order_by(Report.uploaded_at.desc()).limit(20).all()
    return render_template('admin.html', appts=appts, tasks=tasks, reports=reports)

@app.route('/task/<task_id>/complete', methods=['POST'])
def complete_task(task_id):
    task = HumanTask.query.filter_by(id=task_id).first_or_404()
    task.status = 'closed'
    task.completed_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('admin_index'))

# ---- Simple API to list appointments ----
@app.route('/appointments')
def list_appointments():
    appts = Appointment.query.order_by(Appointment.created_at.desc()).limit(100).all()
    out = []
    for a in appts:
        out.append({'id':a.id, 'patient':a.patient_name, 'phone':a.patient_phone, 'doctor':a.doctor, 'scheduled_for':a.scheduled_for.isoformat(), 'status':a.status})
    return jsonify(out)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
