import re
import os
import csv
from collections import defaultdict

def split_sessions(file_content):
    session_pattern = r'=== New Turn ===\nUser: .*?\nAssistant: 1\..*?\n(?:.*?\n)*?=== Post-Session Feedback for Session \d+ ===\nFamiliarity: .*?\(\d+\)\nDifficulty: .*?\(\d+\)'
    
    sessions = {}
    for match in re.finditer(session_pattern, file_content, re.DOTALL):
        session_content = match.group(0)
        
        session_num_match = re.search(r'Session (\d+)', session_content)
        if session_num_match:
            session_num = session_num_match.group(1)
            sessions[session_num] = session_content
    
    return sessions

def extract_dialogue_turn_count(session_content):

    pattern = r'Assistant: (\d+)\.'
    matches = re.findall(pattern, session_content)
    
    if matches:

        numbers = [int(match) for match in matches]
        return max(numbers)
    else:
        return 0

def extract_user_question_count(session_content):

    pattern = r'User: (.*?)\nAssistant: \d+\.'
    matches = re.findall(pattern, session_content)
    
    total_word_count = 0
    user_questions = []
    
    for question in matches:

        words = question.split()
        word_count = len(words)
        total_word_count += word_count
        user_questions.append({
            'question': question,
            'word_count': word_count
        })
    
    return total_word_count, user_questions

def process_conversation_file(file_path):
   
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    sessions = split_sessions(content)
    
    session_data = {}
    for session_num, session_content in sessions.items():
        dialogue_turn_count = extract_dialogue_turn_count(session_content)
        user_question_count, user_questions = extract_user_question_count(session_content)
        
        session_data[session_num] = {
            'content': session_content,
            'dialogue_turn_count': dialogue_turn_count,
            'user_question_count': user_question_count,
            'user_questions': user_questions
        }
    
    return session_data

def process_all_files(folder_path, output_csv):
 
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    
    all_data = []
    
    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        print(f"处理文件: {txt_file}")
        
        try:
            session_data = process_conversation_file(file_path)
            
            for session_num, data in session_data.items():
                all_data.append({
                    'file_name': txt_file,
                    'session_id': session_num,
                    'dialogue_turn_count': data['dialogue_turn_count'],
                    'user_question_count': data['user_question_count']
                })
                
        except Exception as e:
            print(f"处理文件 {txt_file} 时出错: {e}")
    
    if all_data:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['file_name', 'session_id', 'dialogue_turn_count', 'user_question_count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for row in all_data:
                writer.writerow(row)
        
        print(f"成功处理 {len(txt_files)} 个文件，共 {len(all_data)} 个session")
        print(f"结果已保存到: {output_csv}")
    else:
        print("没有找到任何数据")

if __name__ == "__main__":

    folder_path = "."  
    output_csv = "conversation_analysis.csv"
    
    process_all_files(folder_path, output_csv)
    
    try:
        with open(output_csv, 'r', encoding='utf-8') as f:
            print("\nCSV文件预览:")
            print(f.read())
    except FileNotFoundError:
        print("CSV文件未找到")