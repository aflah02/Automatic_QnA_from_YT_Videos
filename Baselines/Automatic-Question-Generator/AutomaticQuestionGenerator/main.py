import aqgFunction
import json, random
import os

def getQuestions(inputText):
    aqg = aqgFunction.AutomaticQuestionGenerator()

    # inputTextPath = "DB//sample_3_para.txt"
    # readFile = open(inputTextPath, 'r+')

    # inputText = readFile.read()

    questionList = aqg.aqgParse(inputText)
    questionList = [q for q in questionList if q != '\n']
    # randomly sample 5 questions
    questionList = random.sample(questionList, 5)

    return questionList

if __name__ == "__main__":
    # main()
    questions = {}
    paths = os.listdir('Data/Chunked_Transcripts')
    json_paths = []
    for path in paths:
        if 'json' in path:
            json_paths.append(path)
    data = {}
    for jpath in json_paths:
        with open('Data/Chunked_Transcripts/' + jpath) as f:
            jdata = json.load(f)
        data[jpath] = jdata
    
    for fname in data.keys():
        questions[fname] = {}
        print("FILE: ", fname)
        transcript = data[fname]
        for val in transcript.keys():
            text = transcript[val]['text']
            # print(text)
            # print()
            # print("AQG Questions:")
            q = getQuestions(text)
            # print(q)
            questions[fname][val] = q
            # print()
    print("========= FILE ENDED =========")

    with open('Baselines\Automatic-Question-Generator\AutomaticQuestionGenerator\AQG_Questions.json', 'w') as outfile:
        json.dump(questions, outfile)