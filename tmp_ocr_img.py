from rapidocr_onnxruntime import RapidOCR

img = r'C:/Users/Administrator/.openclaw/media/inbound/d999a253-2634-481c-86e2-9fd92f2fa726.jpg'
engine = RapidOCR()
res, _ = engine(img)
if not res:
    print('NO_TEXT')
else:
    for i, r in enumerate(res[:200], 1):
        # r: [box, text, score]
        print(f"{i:03d}\t{r[1]}\t{r[2]:.3f}")
