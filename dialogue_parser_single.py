import re

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

if __name__ == "__main__":
    file_path = "Pilot_1_conversation_HWTJXAS8PNR5Z4GF9O2D_2025-10-03_15-23-16.txt"
    
    try:
        session_data = process_conversation_file(file_path)
        
        print(f"共找到 {len(session_data)} 个session:")
        for session_num, data in session_data.items():
            content = data['content']
            dialogue_turn_count = data['dialogue_turn_count']
            user_question_count = data['user_question_count']
            user_questions = data['user_questions']
            
            print(f"\n--- Session {session_num} ---")
            print(f"内容长度: {len(content)} 字符")
            print(f"对话轮次数量 (dialogue_turn_count): {dialogue_turn_count}")
            print(f"用户问题单词总数 (user_question_count): {user_question_count}")

            print("用户问题详情:")
            for i, q in enumerate(user_questions, 1):
                print(f"  问题{i}: '{q['question']}' (单词数: {q['word_count']})")
            
            lines = content.split('\n')
            first_lines = lines[:5]
            last_lines = lines[-5:] if len(lines) > 5 else lines
            
            print("前5行预览:")
            for line in first_lines:
                print(f"  {line}")
            
            print("最后5行预览:")
            for line in last_lines:
                print(f"  {line}")
            
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except Exception as e:
        print(f"处理文件时出错: {e}")
