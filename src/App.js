import MainLogo from "./plainBioWaveHomePage.webp";
import MainTitle from "./path1.jsx";
import "./App.css";

function App() {
  return (
    <body>
      <div class="container">
        {/* First row - two items, one on left, one on right */}
        <div class="row top-row">
          <div class="left-item">
            <img src={MainTitle} className="mainLogo" alt="LeftLogo" />
          </div>
          <div class="right-item">
            <img class="menuLogo" src="{MainLogo}" alt="RightLogo" />
          </div>
        </div>

        {/* Second row - 5 evenly spaced squares */}
        <div class="row middle-row">
          <div class="square">Square 1</div>
          <div class="square">Square 2</div>
          <div class="square">Square 3</div>
          <div class="square">Square 4</div>
          <div class="square">Square 5</div>
        </div>

        {/*  Third row - a single box */}
        <div class="row bottom-row">
          <div class="box">Single Box</div>
        </div>
      </div>
    </body>
  );
}

export default App;
