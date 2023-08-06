from sense_text_extractor import text_extract_pb2, text_extract_pb2_grpc
import grpc
import sense_core as sd


class SenseTextExtractor(object):

    def __init__(self, host=None, port=None, label=None):
        if label and len(label) > 0:
            self.host = sd.config(label, 'host')
            self.port = sd.config(label, 'port')
        else:
            self.host = host
            self.port = port

    def extract_text(self, url, title, html=''):
        channel = grpc.insecure_channel(self.host + ':' + self.port)
        stub = text_extract_pb2_grpc.TextExtractorStub(channel)
        resp = stub.extract(text_extract_pb2.ExtractRequest(url=url, title=title, html=html))
        if resp.code == 0:
            return resp.text
        sd.log_info('extract text failed for ' + url + ' code is ' + str(resp.code))
        return ''
