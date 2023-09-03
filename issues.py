from pypdf import PdfReader

score_path = './test_score.pdf'
bookmark_count = len(PdfReader(score_path).outline)

print(bookmark_count)