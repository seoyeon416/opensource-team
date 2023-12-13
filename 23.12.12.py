import spacy
from collections import Counter
from bokeh.plotting import figure, show
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral11

# spaCy 모델 로드
nlp = spacy.load("en_core_web_sm")

def extract_keywords(sentence):
    # spaCy를 사용하여 명사와 형용사 추출
    doc = nlp(sentence)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]
    return keywords

def get_main_topic(keywords):
    # 가장 빈도가 높은 키워드 선택
    topic_counter = Counter(keywords)
    main_topic = topic_counter.most_common(1)[0][0]
    return main_topic

def recommend_palette(main_topic):
    # 간단한 규칙을 사용하여 주제에 맞는 컬러 팔레트 추천
    if "technology" in main_topic.lower():
        return ["#4285F4", "#0F9D58", "#F4B400", "#DB4437"]
    elif "science" in main_topic.lower():
        return ["#4285F4", "#34A853", "#FBBC05", "#EA4335"]
    elif "art" in main_topic.lower():
        return ["#4285F4", "#AA66CC", "#FFBB33", "#29B6F6"]
    else:
        return ["#4285F4", "#34A853", "#FBBC05", "#EA4335"]

# Bokeh 바 차트 생성
p = figure(x_range=[], height=350, title="Recommended Palette for Topics",
           toolbar_location=None, tools="", y_axis_label="Color Intensity")

# 사용자로부터 여러 문장 입력 받기
user_sentences = input("Enter multiple sentences separated by commas: ")
sentences = user_sentences.split(',')

# 각 문장에 대한 주제어와 컬러 팔레트 출력 및 시각화
for sentence in sentences:
    # 키워드 추출
    keywords = extract_keywords(sentence)
    # 주제어 추출
    main_topic = get_main_topic(keywords)
    # 주제에 맞는 컬러 팔레트 추천
    recommended_palette = recommend_palette(main_topic)
    # 결과 출력
    print(f"Input Sentence: {sentence.strip()}")
    print(f"Main Topic: {main_topic}")
    print(f"Recommended Palette: {recommended_palette}")
    # Bokeh를 사용하여 컬러 팔레트 시각화
    p.vbar(x=recommended_palette, top=[1] * len(recommended_palette), width=0.9,
           color=linear_cmap('x', Spectral11, 0, 1),
           legend_field="x")

    print("\n")

# Bokeh 차트 표시
p.legend.title = 'Topics'
p.legend.label_text_font_size = '10pt'
p.legend.click_policy = "hide"
show(p)
