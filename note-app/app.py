import os
import re
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# 노트 파일 경로
NOTES_FILE = 'notes.json'
BACKUP_DIR = 'backups'  # 백업 폴더 경로

# JSON 파일에서 노트 불러오기
def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# 노트 저장하기
def save_notes(notes):
    with open(NOTES_FILE, 'w', encoding='utf-8') as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)

# 노트를 자동 저장하는 엔드포인트
@app.route('/save_notes', methods=['POST'])
def save_notes_route():
    notes = request.json.get('notes')
    if notes is not None and isinstance(notes, list):
        save_notes(notes)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failed', 'error': 'Invalid notes format'}), 400

# 백업 파일 저장
@app.route('/backup_notes', methods=['POST'])
def backup_notes():
    notes = request.json.get('notes')
    
    if not notes or not isinstance(notes, list) or len(notes) == 0:
        return jsonify({'status': 'failed', 'error': 'No valid notes provided'}), 400

    # 첫 번째 노트의 첫 10글자를 파일 이름으로 사용 (공백 제외)
    first_note = notes[0]

    # 특수 문자를 제거하거나 대체하여 파일 이름을 생성
    safe_filename = re.sub(r'[<>:"/\\|?*]', '_', ''.join(first_note[:10].split())) + '.txt'
    backup_path = os.path.join(BACKUP_DIR, safe_filename)

    # 백업 폴더가 없으면 생성
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # 노트 내용을 txt 파일로 저장
    with open(backup_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(notes))

    return jsonify({'status': 'backup success', 'filename': safe_filename})

# 메인 페이지 - 노트 보기
@app.route('/')
def index():
    notes = load_notes()  # 노트 불러오기
    return render_template('index.html', notes=notes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
