const $responseDiv = $("#responseDiv");
const $form = $("#guess-form");
const $scoreDiv = $("#scoreDiv");
let seconds = 60;

function updateTimerDisplay() {
  $("#timerDiv").html(`Time left: ${seconds} seconds`);
}

const submitGuess = async () => {
  const $word = $("#guessed-word").val();
  const response = await axios.get("/validate", { params: { word: $word } });

  $responseDiv.html(response.data.message);
  $scoreDiv.html(response.data.score);

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
    }
  }, 1000);
}

startGame();
