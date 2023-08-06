from sense_text_extractor import SenseTextExtractor
import sense_core as sd

sd.log_init_config('text_extractor', sd.config('log_path'))


def test_text_extract():
    sd.log_info("xxxxxxx")
    extractor = SenseTextExtractor(label='text_extractor')
    text = extractor.extract_text("http://sports.sina.com.cn/g/pl/2019-01-11/doc-ihqhqcis5048507.shtml", "穆里尼奥在等待复出")
    sd.log_info(text)


def test_text_extract2():
    extractor = SenseTextExtractor('52.83.143.61', '6681')
    text = extractor.extract_text("http://sports.sina.com.cn/g/pl/2019-01-11/doc-ihqhqcis5048507.shtml", "穆里尼奥在等待复出")
    print(text)
