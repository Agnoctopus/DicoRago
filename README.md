# DicoRago

**Learn Korean more efficiently with DicoRago!**

DicoRago is a web application designed to help you analyze and understand Korean texts by exploring its vocabulary and grammatical structures. Whether you're a **beginner** or an **advanced learner**, DicoRago makes learning smarter by breaking down texts, highlighting words you know, and helping you deepen your understanding of new ones.

**Try it now at [dicorago.com](https://dicorago.com/)**!

<p  align="center">
  <a href="https://github.com/user-attachments/assets/97d315b0-fc41-4fb1-b2c2-3d53cb75e07c">
    <img src="https://github.com/user-attachments/assets/096e55f9-dec6-4bc5-be9b-18e0c8eafae6" alt="animated" />
  </a>  
</p>

## Features

- **Vocabulary analysis**: Paste any Korean text and get an immediate breakdown with translations.
- **Color-coded word recognition**: Easily identify known and unknown words for a more efficient learning process.
- **Vocabulary filtering**: Hide words you already know and focus on new ones.
- **In-depth word exploration**: Access multiple meanings, definitions, and example sentences.
- **Personal dictionary management**:  Track your progress by saving new words to your vocabulary list.
- **Grammar structure analysis**: Get word types and sentence constructions to improve comprehension.

## Why use DicoRago?

- **Save time** by quickly identifying unknown words.
- **Learn in context** with clear definitions and example sentences.
- **Tailor your learning** by building your personal vocabulary list.
- **Master grammar** by exploring sentence structures.

## Technologies

DicoRago is built with a modern tech stack to ensure speed, reliability, and a smooth user experience:

- **Backend**: FastAPI powered by [Khaiii](https://github.com/Agnoctopus/ModernKhaiii) for morphological analysis.
- **Frontend**: Vue 3 with TypeScript and Tailwind CS for a nice and responsive interface.

### Prerequisites

Before running DicoRago, make sure you have:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Running the application

Simply run the following command in the project root:

```sh
docker-compose up --build
```

This will:

1. Build and launch the backend and frontend services.
2. Start the backend at [http://localhost:8000](http://localhost:8000).
3. Start the frontend at [http://localhost:8080](http://localhost:8080).

Go to [http://localhost:8080](http://localhost:8080) and Enjoy your personalized Korean learning journey with DicoRago! 🎉

## Contributions

Contributions are welcome! If you find a bug, have suggestions, or want to add new features, feel free to **open an issue** or **submit a pull request**.

## License

DicoRago is open-source and released under the **GNU AGPL** license.
