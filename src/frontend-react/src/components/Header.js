import { useContext } from "react";
import { FileContext } from "../FileContext";
import { useNavigate, Link } from "react-router-dom";
import { Typography, Button } from "antd";
const { Title } = Typography;

const Header = () => {
  const { result } = useContext(FileContext);
  const navigate = useNavigate();
  return (
    <header>
      <div
        style={{
          margin: "0 100px",
          borderBottom: "1px solid #e8e8e8",
        }}
      >
        <Title style={{ display: "inline-block" }}>
          <span
            onClick={() => {
              navigate("/");
            }}
            className="link"
          >
            Toonranslator
          </span>
        </Title>
        <div
          style={{
            marginLeft: "20px",
            display: "inline-block",
          }}
        >
          <Link to="/">Home</Link> &nbsp;
          <Link to="/demo">Demo</Link> &nbsp;
          <Link to="/result">Result</Link> &nbsp;
          <Link to="/edit">Edit</Link> &nbsp;
          <Link to="/loading">Loading</Link> &nbsp;
        </div>
        <Button
          onClick={() => {
            console.log(result);
          }}
        >
          디버그
        </Button>
      </div>
    </header>
  );
};

export default Header;
