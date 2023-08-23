class Score:
    Title = ""
    Author = [""] # Composers / Arrangers
    Subject = [""] # Genres - Swing, Vocal, Latin, Rock etc
    Keywords = [""] # Tags - Part name e.g. Tenor Sax 2
    
    def __init__(self, Title, Author, Subject, Keywords):
        self.Title = Title
        self.Author = Author
        self.Subject = Subject
        self.Keywords = Keywords
        
    def __str__(self) -> str:
        result = "\n~ Score Metadata ~"
        for i in self.__dict__:
            result += "\n"
            result += i.capitalize()
            result += ": "
            j = getattr(self, i)
            result += str(j)
            
        return result
            