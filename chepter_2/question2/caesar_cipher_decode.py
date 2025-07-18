import string


#2. 카이사르의 암호를 풀 수 있는 함수를 caesar_cipher_decode() 라는 이름으로 만든다.
#3. caesar_cipher_decode() 함수는 풀어야 하는 문자열을 파라메터로 추가한다. 이때 파라메터의 이름은 target_text으로 한다.
def caesar_cipher_decode(target_text):
    # '0'은제자리 이므로 의미가 없음
    results =[]
    #4.caesar_cipher_decode() 에서 자리수에 따라 암호표가 바뀌게 한다. 자리수는 알파벳 수만큼 반복한다.
    for shift in range(1, 26):
        result = ''
        for char in target_text:
            #소문자일경우 아스키코드로 변환
            if char.islower():
                idx = (ord(char) - ord('a') - shift) % 26
                result += chr(ord('a') + idx)
            elif char.isupper():
                idx = (ord(char) - ord('A') - shift) % 26
                result += chr(ord('A') + idx)
            else:
                result += char
        results.append((shift, result))
    return results

if __name__ == '__main__':
    #1. password.txt 파일을 읽어온다.
    try:
        with open('chepter_2/question2/password.txt', 'r', encoding='utf-8') as f:
            target_text = f.read()
    except FileNotFoundError():
        print("파일을 찾을 수 없습니다.")
        exit()

    #5. 자리수에 따라서 해독된 결과를 출력한다.
    result_texts = caesar_cipher_decode(target_text)
    for idx, result_text in result_texts:
        print(f'{idx} : {result_text}')

    #6. 몇 번째 자리수로 암호가 해독되는지 찾아낸다. 눈으로 식별이 가능하면 해당 번호를 입력하면 그 결과를 result.txt로 저장을 한다.
    selected = int(input(" 몇 번째 자리수로 암호가 해독되는지 찾아낸다. : "))
    # index는 0부터 시작
    final_text = result_texts[selected - 1][1]  
    try:
        with open('chepter_2/question2/result.txt', 'w', encoding='utf-8') as f:
            f.write(final_text)
    except Exception as e:
        print(e)