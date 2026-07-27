class ScrapperError(Exception):
    def __init__(self,message,file,url,xpath,city):
        self.message=message
        self.file=file
        self.url=url
        self.xpath=xpath
        self.city=city
        super().__init__(self.message)