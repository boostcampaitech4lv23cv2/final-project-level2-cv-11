import { Typography, Divider } from "antd";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";

const { Title, Text, Link } = Typography;

const Button = styled.button`
  width: 160px;
  height: 80px;
  border-radius: 20px;
  border: none;
  margin-top: 20px;
  background: deepskyblue;
  font-size: 22px;
  font-weight: bold;
  color: white;
  &:hover {
    cursor: pointer;
  }
`;

const Main = () => {
  const navigate = useNavigate();
  return (
    <div style={{ margin: "0 100px 100px" }}>
      <div style={{ height: "20px" }} />
      <div className="mb-28">
        <Title className="text-center">메인 페이지 작업중</Title>

        <div className="flex justify-center">
          <Button
            onClick={() => {
              navigate("/demo");
            }}
          >
            시작하기
          </Button>
        </div>
        <div className="mb-32" />

        <Title level={5}>
          웹툰 번역 자동화 프로젝트 Toonranslator의 홈페이지 입니다.
        </Title>

        <Text>프로젝트 소개, 관련 사진 등 추가 예정</Text>
        <br />

        <Title level={5}>1. 웹툰 사업의 발전</Title>
        <Text>
          80~10까지의 인쇄 만화(만화책, 만화잡지) 시장이 호황을 뒤로하고
          스마트폰을 필두로 한 디지털화가 가속화되면서, 전 세계적으로 디지털
          만화 컨텐츠의 접근성이 크게 올라갔다. 이러한 변화에 따라, 디지털
          만화시장은 현재 기존의 인쇄 만화시장의 점유율을 상회하는 영향력을
          보여주고 있다.
        </Text>
        <Title level={5}>2. 글로벌 웹툰 시장과 컨텐츠</Title>
        <Text>
          디지털 만화시장의 대표 주자인 한국의 웹툰의 경우, 그 시장이 커짐에
          따라 해외에도 플랫폼 형식으로 진출하며 호성적을 내고 있다. 이는 비단
          웹툰(ex.네이버 웹툰, 카카오 페이지)의 플랫폼 형식이 사용자가 느끼기에
          편리하고 뛰어난 직관성을 가지고 있기 때문만이 아니라 타국의 컨텐츠를
          서비스 국가에 번역 후 제공하였기 때문이다. 일본에 진출하여 일본 웹툰
          플랫폼 1위를 하고 있는 “라인 망가(네이버)”나 일본에서
          서비스하는“픽코마(카카오)”의 경우를 보면, 매출 상위 랭크에 일본의
          작품뿐만이 아니라 한국과 중국, 미국 등 해외의 ip 컨텐츠가 있다. 또한,
          북미 WEBTOON(네이버)에서 시작해 큰 인기를 끌었던 “로어 올림푸스”도
          네이버 웹툰을 통해 우리나라에 정식 번역되며 좋은 평가를 얻었다. 이러한
          사례들을 통해 웹툰 사업의 발전은 접근성과 편의성을 필두로 한 플랫폼
          사업 운영과 국제적인 컨텐츠를 플랫폼 내로 가져와 서비스하는 ip 산업에
          달려있다는 결론을 낼 수 있다.
        </Text>
        <Title level={5}>3. 웹툰 번역의 필요성과 효과음 번역의 어려움</Title>
        <Text>
          국제적인 웹툰, ip 컨텐츠의 교류가 무엇보다 필요한 상황에서 가장
          걸림돌이 되는 것은 언어번역이다. 아무리 좋은 컨텐츠라도 자국의 언어로
          번역되어 있지 않으면 접근성이 매우 낮아지고 컨텐츠의 진가를 알아보고
          어렵다. 이를 해결하기 위해 웹툰의 대사뿐만이 아니라 상황과 맥락에 맞는
          번역을 해주는 “웹툰 번역가”라는 직업이 새로 등장하였고, 글로벌 웹툰
          시장이 커짐에 따라 웹툰 번역 시장도 같이 성장할 것으로 예측된다. 웹툰
          번역가의 직무는 크게 “번역”과 “편집”으로 나눌 수 있다. “번역”은 기존의
          번역가들이 했던 일처럼, 문화와 국가에 맞게 언어를 자연스럽게 변환하는
          일이며, “편집”은 변환된 언어가 웹툰 그림에 자연스럽게 들어가도록
          포토샵 등을 사용해 그리거나 써넣는 일이다. 2 말풍선 안에 있는 전형적인
          텍스트의 편집은 만화 전반적으로 비슷한 폰트를 사용하고 기본적으로
          말풍선이라는 틀 안에 존재하기 때문에 크게 어렵지 않으나, 그림 속에
          존재하고 원작가가 그려 넣는 경우가 많아 특별한 폰트가 존재하지 않는
          효과음은 언어의 style에 맞게 다시 그려 넣어야 하기 때문에 작업 시간과
          노력이 많이 들고 자동화가 어려워지는 큰 원인이 되고 있다.
        </Text>

        <br />
      </div>

      <Divider />

      <div className="mb-28">
        <Title>아키텍처</Title>
        <Title level={5}>프로젝트 아키텍처를 설명합니다</Title>
        <img src="/arch.png" />
      </div>

      <Divider />

      <div className="mb-28">
        <Title>팀 소개</Title>
        <Title level={5}>저희 팀을 소개합니다</Title>
      </div>
    </div>
  );
};

export default Main;
