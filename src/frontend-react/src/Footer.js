import React from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGithub } from "@fortawesome/free-brands-svg-icons";

const GithubButton = () => {
  const handleClick = () => {
    window.location.href =
      "https://github.com/boostcampaitech4lv23cv2/final-project-level2-cv-11";
  };

  return (
    <button
      onClick={handleClick}
      style={{
        backgroundColor: "#333",
        color: "white",
        padding: "0.5em 1em",
        borderRadius: "3px",
        cursor: "pointer",
        display: "inline-block",
        marginTop: "1em",
      }}
    >
      <FontAwesomeIcon
        icon={faGithub}
        style={{ marginRight: "0.5em", fontSize: "1.2em" }}
      />
      Visit GitHub Project Page
    </button>
  );
};

const Footer = () => {
  return (
    <footer
      style={{
        backgroundColor: "#333",
        color: "white",
        padding: "2em",
        textAlign: "center",
        borderTop: "1px solid white",
      }}
    >
      <p>부스트캠프 AI Tech 4기</p>
      <p>CV 11조 구미호</p>
      <GithubButton />
    </footer>
  );
};

export default Footer;
