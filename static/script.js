const $responseDiv = $("#responseDiv");
const $form = $("#guess-form");

const submitGuess = async () => {
  const $word = $("#guessed-word").val();
  const response = await axios.get("/validate", { params: { word: $word } });

  $responseDiv.html(response.data.message);
};

$form.on("submit", async (event) => {
  event.preventDefault();
  submitGuess();
});
