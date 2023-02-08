import { fabric } from "fabric";
import FontList from "./FontList";

export const newRect = (props) => {
  const box = new fabric.Rect({
    top: 0,
    left: 0,
    height: 100,
    width: 100,
    fill: "rgba(0, 0, 0, 0.1)",
    stroke: "red",
    strokeWidth: 1,
  });
  box.textKor = "";
  box.textEng = "";
  box.fontFamily = FontList[0]["name"];
  box.fontSize = 40;
  box.color = "black";
  for (const key in props) {
    box[key] = props[key];
  }
  return box;
};

export function calculateFontSize(text, width, height, fontFamily = "arial") {
  let fontSize = 1;
  let textbox = new fabric.Textbox(text, {
    width: width,
    fontSize: fontSize,
    fontFamily,
    textAlign: "center",
  });

  while (textbox.height < height && textbox.width < width * 1.3) {
    fontSize += 1;
    textbox = new fabric.Textbox(text, {
      width: width,
      fontSize: fontSize,
      fontFamily,
      textAlign: "center",
    });
  }

  return fontSize - 1;
}

export const rect2textbox = (rect) => {
  if (rect.get("type") === "textbox") return rect;
  const fontsz = calculateFontSize(
    rect.textEng,
    rect.width * rect.scaleX,
    rect.height * rect.scaleY,
    rect.fontFamily
  );
  rect.setFontSize(fontsz);
  const textbox = new fabric.Textbox(rect.textEng, {
    width: rect.width * rect.scaleX,
    fontFamily: rect.fontFamily,
    fontSize: fontsz,
    textAlign: "center",
  });
  for (const key of [
    "id",
    "top",
    "left",
    // "width",
    // "height",
    // "fontFamily",
    // "fontSize",
    "textKor",
    "textEng",
    "recFonts",
    "layer",
    "color",
  ]) {
    textbox[key] = rect[key];
  }
  return textbox;
};
