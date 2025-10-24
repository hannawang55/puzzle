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

def process_conversation_file(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    sessions = split_sessions(content)
    
    session_data = {}
    for session_num, session_content in sessions.items():
        dialogue_turn_count = extract_dialogue_turn_count(session_content)
        session_data[session_num] = {
            'content': session_content,
            'dialogue_turn_count': dialogue_turn_count
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
            
            print(f"\n--- Session {session_num} ---")
            print(f"内容长度: {len(content)} 字符")
            print(f"对话轮次数量 (dialogue_turn_count): {dialogue_turn_count}")
            
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到")
    except Exception as e:
        print(f"处理文件时出错: {e}")