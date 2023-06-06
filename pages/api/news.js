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
    const chatId = "pvxtechnews";
    const kryptonId = 649341653;

    const botTG = new TelegramBot(token, { polling: false });
    const message = await getNews();

    botTG.sendMessage(kryptonId, message);
    res.status(200).json({ name: "news posted!" });
  } catch (error) {
    console.log(error);
    res.status(200).json({ name: error.toString() });
  }
}
