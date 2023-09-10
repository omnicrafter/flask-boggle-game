const $responseDiv = $("#responseDiv");
const $form = $("#guess-form");
const $scoreDiv = $("#scoreDiv");
const $playCountDiv = $("#playCountDiv");
let seconds = 60;
let playCount = 0;
const $playAgainButton = $("#playAgainButton");

function updateTimerDisplay() {
  $("#timerDiv").html(`Time left: ${seconds} seconds`);
}

const submitGuess = async () => {
  const $word = $("#guessed-word").val();
  const response = await axios.get("/validate", { params: { word: $word } });
  playCount = response.data.playCount;

  $responseDiv.html(response.data.message);
  $scoreDiv.html(`Your score: ${response.data.score}`);

  $("#guessed-word").val("");
};

$form.on("submit", async (event) => {
  event.preventDefault();
  submitGuess();
});

function startGame() {
  updateTimerDisplay();
  const gameInterval = setInterval(function () {
    seconds--;
    updateTimerDisplay();
    if (seconds < 0) {
      $("#timerDiv").html(`Time left: 0 seconds`);
      clearInterval(gameInterval);
      $form.prop("disabled", true);
      $responseDiv.html("Time's up! Game over");

      playCount += 1;

      sendPlayCount();
      $playCountDiv.html(`You have played ${playCount} times.`);
    }
  }, 1000);
}

startGame();

const sendPlayCount = async () => {
  const response = axios.post("/record_playcount", { playCount });

  return "Playcount Sent Successfully";
};

// Add a click event listener to the play again button
$playAgainButton.on("click", function () {
  window.location.href = "/";
});
