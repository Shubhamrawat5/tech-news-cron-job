const TelegramBot = require("node-telegram-bot-api");
const axios = require("axios");

const getNews = async () => {
  let url = "https://pvx-api-vercel.vercel.app/api/news";
  const { data } = await axios.get(url);

  let msg = `☆☆☆💥 Tech News 💥☆☆☆`;
  let inshorts = data.inshorts;
  let count = 0; //for first 14 news only
  for (let i = 0; i < inshorts.length; ++i) {
    ++count;
    if (count === 15) break;
    msg += `\n\n🌐 ${inshorts[i]}`;
  }
  msg += `\n\njoin TG@pvxtechnews for daily tech news!`;
  return msg;
};

export default async function handler(req, res) {
  try {
    const token = process.env.token; //tg bot token here
    const chatId = "@pvxtechnews";
    const kryptonId = 649341653;

    const botTG = new TelegramBot(token, { polling: false });
    console.log("Fetching tech news...");
    const message = await getNews();
    console.log(message);

    console.log("Posting news to TG channel...");
    await botTG.sendMessage(chatId, message);
    console.log("Tech news posted.");

    res.status(200).json({ news: message });
  } catch (error) {
    console.log(error);
    res.status(200).json({ news: error.toString() });
  }
}
