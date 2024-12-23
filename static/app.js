class Chatbot {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"),
    };

    this.state = false;
    this.messages = [];
    this.welcomeDisplayed = false;
  }

  display() {
    const { openButton, chatBox, sendButton } = this.args;
    openButton.addEventListener("click", () => this.toggleState(chatBox));
    sendButton.addEventListener("click", () => this.onSendButton(chatBox));
    const node = chatBox.querySelector("input");
    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }

  toggleState(chatbox) {
    this.state = !this.state;

    if (this.state) {
      if (!this.welcomeDisplayed) {
        this.addWelcome(chatbox);
        this.welcomeDisplayed = true;
      }
      chatbox.classList.add("chatbox--active");
    } else {
      chatbox.classList.remove("chatbox--active");
    }
  }

  addWelcome(chatbox) {
    let text1 = "Hello there! Describe what you want to design.";
    let msg1 = { name: "AI", message: text1 };
    this.messages.push(msg1);
    this.updateChatText(chatbox);
  }

  onSendButton(chatbox) {
    var textField = chatbox.querySelector("input");
    let text1 = textField.value;
    textField.value = "";
    if (text1 === "") return;

    let msg1 = { name: "You", message: text1 };
    this.messages.push(msg1);

    const loadingGif = document.getElementById("loading-gif");
    loadingGif.src = "../static/images/icons8-loading-infinity.gif";

    fetch($SCRIPT_ROOT + "/predict_v1", {
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((r) => {
        console.info(r.answer);
        let answer = r.answer;

        let msg2 = { name: "AI", message: answer };

        this.messages.push(msg2);

        loadingGif.src = "static/images/icons8-loading-infinity-static.png";

        this.updateChatText(chatbox);
      })
      .catch((error) => {
        console.error("Error:", error);
        this.updateChatText(chatbox);
      });
  }

  updateChatText(chatbox) {
    var html = "";
    let name = "You";
    this.messages
      .slice()
      .reverse()
      .forEach(function (item) {
        if (name.localeCompare(item.name) == 0) {
          html +=
            '<div class="messages__item messages__item--visitor">' +
            item.name +
            ": " +
            item.message +
            "</div>";
        } else {
          html +=
            '<div class="messages__item messages__item--operator">' +
            item.name +
            ": " +
            item.message +
            "</div>";
        }
      });

    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
  }
}

const chatbot = new Chatbot();
chatbot.display();
