import aqgFunction

def main():
    aqg = aqgFunction.AutomaticQuestionGenerator()

    inputTextPath = "DB//sample_3_para.txt"
    readFile = open(inputTextPath, 'r+')

    inputText = readFile.read()

    questionList = aqg.aqgParse(inputText)
    aqg.display(questionList)

    return 0

def convert_transcriptions_to_paragraph_text():
    filtered_text = []
    with open("DB/sample_3.txt", "r", encoding="utf8") as f:
        text = f.readlines()
    for i in range(len(text)):
        if i%2==0:
            filtered_text.append(text[i])
    text = " ".join(filtered_text)
    with open("DB/sample_3_para.txt", "w") as f:
        f.write(text.replace("\n", " "))

if __name__ == "__main__":
    main()
    # convert_transcriptions_to_paragraph_text()
