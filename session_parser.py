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

def process_conversation_file(file_path):
    """
    处理对话文件，返回各个session
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    sessions = split_sessions(content)
    
    return sessions

if __name__ == "__main__":
    file_path = "Pilot_1_conversation_HWTJXAS8PNR5Z4GF9O2D_2025-10-03_15-23-16.txt"
    
    try:
        sessions = process_conversation_file(file_path)
        
        print(f"共找到 {len(sessions)} 个session:")
        for session_num, content in sessions.items():
            print(f"\n--- Session {session_num} ---")
            print(f"内容长度: {len(content)} 字符")
            
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