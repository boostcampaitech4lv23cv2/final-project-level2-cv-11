import { useContext, useState, useEffect } from "react";
import { GlobalContext } from "../GlobalContext";
import { message, Button } from "antd";
import { newRect } from "../utils";

const OCRButton = ({ setBoxes, canvas }) => {
  const { files, step, setStep, backendHost, idRef } =
    useContext(GlobalContext);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (files.typical && files.untypical && step == 10) onClick();
  }, [step, files]);

  const onClick = async () => {
    if (!files.typical || !files.untypical) {
      message.error("파일을 먼저 업로드해주세요.");
      return;
    }

    setLoading(true);
    const boxes = [];

    const formData = new FormData();
    formData.append("file", files.typical);
    const p1 = fetch(`${backendHost}txt_extraction/v2`, {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        for (let i = 0; i < data.length; i++) {
          const { x1, y1, w, h, text, fonts, color } = data[i];
          const box = newRect({
            left: x1,
            top: y1,
            width: w,
            height: h,
            textKor: text,
            textEng: "-",
            recFonts: fonts,
            fontFamily: fonts[0]["name"],
            id: idRef.current++,
            layer: "대사",
            color,
          });
          boxes.push(box);
          canvas.add(box);
        }
      });

    const boxes_untypical = [];
    const untypicalFormData = new FormData();
    untypicalFormData.append("file", files.untypical);
    const p2 = fetch(`${backendHost}untypical/txt_extraction/v2`, {
      method: "POST",
      body: untypicalFormData,
    })
      .then((response) => response.json())
      .then((data) => {
        for (let i = 0; i < data.length; i++) {
          const { x1, y1, w, h, text, fonts, color } = data[i];
          const box = newRect({
            left: x1,
            top: y1,
            width: w,
            height: h,
            textKor: text,
            textEng: "-",
            recFonts: fonts,
            fontFamily: fonts[0]["name"],
            id: idRef.current++,
            layer: "효과음",
            color,
          });
          boxes_untypical.push(box);
          boxes.push(box);
          canvas.add(box);
        }
      });

    const p3 = p2.then(() => {
      if (step == 10) setStep(11);
      const ref_fonts = boxes_untypical.map((box) => box.fontFamily + ".ttf");

      const body = JSON.stringify({
        classified_font: ref_fonts,
        en_list: Array(ref_fonts.length).fill(
          "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        ),
      });
      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body,
      };

      const fetchGeneration = (type, idx) => {
        return fetch(`${backendHost}untypical/generation/${type}`, options)
          .then((res) => res.json())
          .then((uris) => {
            if (uris.length != boxes_untypical.length) {
              console.error(
                `효과음 개수 (${boxes_untypical.length})와 생성된 폰트 개수 (${uris.length})가 일치하지 않습니다.))`
              );
            }
            const fs = [];
            for (
              let i = 0;
              i < Math.min(uris.length, boxes_untypical.length);
              i++
            ) {
              const uri = uris[i].replace(/^"/, "").replace(/"$/, "");
              const f = fetch(uri)
                .then((res) => res.blob())
                .then((blob) => blob.arrayBuffer())
                .then((ab) => {
                  const name = `Generated-${type}-${idRef.current++}`;
                  const font = new FontFace(name, ab);
                  console.log("font added", name);
                  font
                    .load()
                    .then((e) => {
                      document.fonts.add(font);
                    })
                    .catch((e) => {
                      console.error("error", font.family, e);
                    });
                  // mxfont를 기본 폰트로 설정
                  if (idx == 2) boxes_untypical[i].fontFamily = name;
                  boxes_untypical[i].recFonts.push({
                    name,
                    prob: `생성 ${idx}`,
                  });
                })
                .catch((e) => {
                  console.error("error", e);
                });
              fs.push(f);
            }
            return Promise.all(fs);
          });
      };

      const f1 = fetchGeneration("mx", 1);
      const f2 = fetchGeneration("gasnext", 2);
      return Promise.all([f1, f2]);
    });

    await Promise.all([p1, p2])
      .then(async () => {
        console.log("then", boxes);
        message.success("OCR에 성공했습니다.");
        canvas.remove(...canvas.getObjects("rect"));
        boxes.sort((a, b) => a.top - b.top);
        boxes.forEach((box) => {
          canvas.add(box);
        });
        await p3;
        setBoxes(boxes);
        if (Math.floor(step / 10) == 1)
          setTimeout(() => {
            setStep(20);
          }, 1000);
      })
      .catch((e) => {
        console.error(e);
        message.error("OCR에 실패했습니다.");
        if (step != 0) setStep(-1);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <>
      <Button id="ocr-button" loading={loading} onClick={onClick}>
        1. OCR 수행
      </Button>
    </>
  );
};

export default OCRButton;
