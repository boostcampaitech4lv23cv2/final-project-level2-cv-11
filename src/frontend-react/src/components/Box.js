import { useState, useEffect } from 'react'
import { Input, Select, Button, InputNumber, message } from 'antd'
import { RightOutlined } from '@ant-design/icons';

const { TextArea } = Input;
const { Option } = Select;

const FontList = [
  {
    name: '나눔고딕',
    value: 'NanumGothic',
  },
  {
    name: '서울한강B',
    value: 'SeoulHangangB.ttf',
  }
]

const Box = ({ i, rect, delBox, convertBox, renderAll }) => {
  const [textKor, setTextKor] = useState(rect.textKor)
  const [textEng, setTextEng] = useState(rect.textEng)
  const [font, setFont] = useState(rect.fontFamily)
  const [fontSize, setFontSize] = useState(rect.fontSize)
  const { x: x1, y: y1 } = rect.getPointByOrigin('left', 'top')
  const { x: x2, y: y2 } = rect.getPointByOrigin('right', 'bottom')

  const [x, setX] = useState(0)
  rect.refresh = ({ text }) => {
    setX(x => x+1)
    setTextEng(text)
  }
  useEffect(() => {
    rect.textKor = textKor
    rect.text = rect.textEng = textEng
    rect.fontFamily = font
    rect.fontSize = fontSize
    renderAll()
  }, [textKor, textEng, font, fontSize])

  useEffect(() => {
    if (textKor !== '')
      onTranslate()
  }, [])

  const [tLoading, setTLoading] = useState(false)
  const onTranslate = () => {
    setTLoading(true)
    fetch('http://49.50.160.104:30002/mt/?' + new URLSearchParams({
      text: textKor
    }), {
      method: 'POST',
    })
      .then(res => res.json())
      .then(res => {
        setTextEng(res)
        setTLoading(false)
      })
      .catch(err => {
        console.error(err)
        message.error('번역에 실패했습니다.')
        setTLoading(false)
      })
  }

  const PadInputNumber = (props) => {
    return <InputNumber
      style={{
        padding: '0 2px'
      }}
      {...props} />
  }

  return <div
    style = {{
      margin: 10,
      padding: 5,
      border: '1px solid black',
    }}
  >
    <div
      style={{
        textAlign: 'center',
      }}
    >
    대사 #{i}
    <div
      style={{
        // position: 'relative',
        top: 0,
        right: 0,
        margin: '0 0 0 10'
      }}
    >
      <Button>인식(미구현)</Button>
      <Button onClick={onTranslate} loading={tLoading}>번역</Button>
      <Button onClick={convertBox}>변환</Button>
      <Button onClick={delBox} danger>삭제</Button>
    </div></div>
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
      }}
    >
      <div
        style = {{
          padding: 5,
          width: '100%',
        }}
      >
        한국어 대사
        <TextArea
          onChange={event => {
            setTextKor(event.target.value)
          }}
          value={textKor}
          autoSize />
      </div>
      <div style={{
        marginTop: 21,
        display: 'flex',
        alignItems: 'center',
      }}>
        <RightOutlined />
      </div>
      <div
        style={{
          padding: 5,
          width: '100%',
        }}
      >
        영어 대사
        <TextArea
          onChange={event => {
            setTextEng(event.target.value)
          }}
          value={textEng}
          autoSize />
      </div>
    </div>
    <div
      style={{
        padding: 10
      }}
    >
      위치
      <div style={{
        display: 'flex',
      }}>
      <PadInputNumber addonBefore={"X"} value={Math.round(x1)} />
      <PadInputNumber addonBefore={"Y"} value={Math.round(y1)} />
      <PadInputNumber addonBefore={"W"} value={Math.round(x2-x1)} />
      <PadInputNumber addonBefore={"H"} value={Math.round(y2-y1)} />
      </div>
    </div>
    <div>
      폰트
      <div>
        <Select
          style={{
            width: 180
          }}
          // defaultValue={'NanumGothic'}
          value={font}
          onSelect={value => {
            setFont(value)
          }}
        >
          {FontList.map(({name, value}) => {
            return <Option value={value}>{name}</Option>
          })}
        </Select>
        <Select
          style={{
            width: 100
          }}
          value={fontSize}
          onSelect={value => {
            setFontSize(value)
          }}
        >
          {
            [32, 36, 40, 44, 48, 52].map(value => {
              return <Option value={value}>{value}</Option>
            })
          }
        </Select>
      </div>
    </div>
  </div>
}

export default Box;