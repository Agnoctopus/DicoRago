export const sampleData = {
  text: `
안녕하세요?
저는 요즘 한국어를 열심히 공부하고 있어요! Dicorago 앱 덕분에 공부가 훨씬 즐거워졌어요~~ 어려운 단어들도 보기 쉽게 정리되어 있고, 한눈에 들어오고, 이해하기 쉬워요. 매일 조금씩 실력이 느는 게 느껴져요!!
공부가 놀이처럼 바뀐 것 같아요!
  `,
  learnedVocab: [
    '안녕',
    '요즘',
    '공부',
    '저',
    '있다',
    '보다',
    '쉽다',
    '이해',
    '덕분',
    '매일',
    '단어',
    '느끼다',
    '한국어',
    '바뀌다',
    '것',
    '같다',
  ],
  units: [
    {
      surface: '안녕하시어요?',
      morphs: [
        { lex: '안녕', tag: 'NNG' },
        { lex: '하', tag: 'XSA' },
        { lex: '시', tag: 'EP' },
        { lex: '어요', tag: 'EF' },
        { lex: '?', tag: 'SF' },
      ],
      word: '안녕하세요?',
      vocabulary: '안녕',
    },
    {
      surface: '저는',
      morphs: [
        { lex: '저', tag: 'NP' },
        { lex: '는', tag: 'JX' },
      ],
      word: '저는',
      vocabulary: '저',
    },
    { surface: '요즘', morphs: [{ lex: '요즘', tag: 'NNG' }], word: '요즘', vocabulary: '요즘' },
    {
      surface: '한국어를',
      morphs: [
        { lex: '한국어', tag: 'NNP' },
        { lex: '를', tag: 'JKO' },
      ],
      word: '한국어를',
      vocabulary: '한국어',
    },
    {
      surface: '열심히',
      morphs: [{ lex: '열심히', tag: 'MAG' }],
      word: '열심히',
      vocabulary: '열심히',
    },
    {
      surface: '공부하고',
      morphs: [
        { lex: '공부', tag: 'NNG' },
        { lex: '하', tag: 'XSV' },
        { lex: '고', tag: 'EC' },
      ],
      word: '공부하고',
      vocabulary: '공부',
    },
    {
      surface: '있어요!',
      morphs: [
        { lex: '있', tag: 'VX' },
        { lex: '어요', tag: 'EF' },
        { lex: '!', tag: 'SF' },
      ],
      word: '있어요!',
      vocabulary: '있다',
    },
    {
      surface: 'Dicorago',
      morphs: [{ lex: 'Dicorago', tag: 'SL' }],
      word: 'Dicorago',
      vocabulary: undefined,
    },
    { surface: '앱', morphs: [{ lex: '앱', tag: 'NNG' }], word: '앱', vocabulary: '앱' },
    {
      surface: '덕분에',
      morphs: [
        { lex: '덕분', tag: 'NNG' },
        { lex: '에', tag: 'JKB' },
      ],
      word: '덕분에',
      vocabulary: '덕분',
    },
    {
      surface: '공부가',
      morphs: [
        { lex: '공부', tag: 'NNG' },
        { lex: '가', tag: 'JKS' },
      ],
      word: '공부가',
      vocabulary: '공부',
    },
    { surface: '훨씬', morphs: [{ lex: '훨씬', tag: 'MAG' }], word: '훨씬', vocabulary: '훨씬' },
    {
      surface: '즐겁어지었어요~',
      morphs: [
        { lex: '즐겁', tag: 'VA' },
        { lex: '어', tag: 'EC' },
        { lex: '지', tag: 'VX' },
        { lex: '었', tag: 'EP' },
        { lex: '어요', tag: 'EC' },
        { lex: '~', tag: 'SO' },
      ],
      word: '즐거워졌어요~~',
      vocabulary: '즐겁다',
    },
    {
      surface: '어렵ㄴ',
      morphs: [
        { lex: '어렵', tag: 'VA' },
        { lex: 'ㄴ', tag: 'ETM' },
      ],
      word: '어려운',
      vocabulary: '어렵다',
    },
    {
      surface: '단어들도',
      morphs: [
        { lex: '단어', tag: 'NNG' },
        { lex: '들', tag: 'XSN' },
        { lex: '도', tag: 'JX' },
      ],
      word: '단어들도',
      vocabulary: '단어',
    },
    {
      surface: '보기',
      morphs: [
        { lex: '보', tag: 'VV' },
        { lex: '기', tag: 'ETN' },
      ],
      word: '보기',
      vocabulary: '보다',
    },
    {
      surface: '쉽게',
      morphs: [
        { lex: '쉽', tag: 'VA' },
        { lex: '게', tag: 'EC' },
      ],
      word: '쉽게',
      vocabulary: '쉽다',
    },
    {
      surface: '정리되어',
      morphs: [
        { lex: '정리', tag: 'NNG' },
        { lex: '되', tag: 'XSV' },
        { lex: '어', tag: 'EC' },
      ],
      word: '정리되어',
      vocabulary: '정리',
    },
    {
      surface: '있고,',
      morphs: [
        { lex: '있', tag: 'VX' },
        { lex: '고', tag: 'EC' },
        { lex: ',', tag: 'SP' },
      ],
      word: '있고,',
      vocabulary: '있다',
    },
    {
      surface: '한눈에',
      morphs: [
        { lex: '한눈', tag: 'NNG' },
        { lex: '에', tag: 'JKB' },
      ],
      word: '한눈에',
      vocabulary: '한눈',
    },
    {
      surface: '들어오고,',
      morphs: [
        { lex: '들어오', tag: 'VV' },
        { lex: '고', tag: 'EC' },
        { lex: ',', tag: 'SP' },
      ],
      word: '들어오고,',
      vocabulary: '들어오다',
    },
    {
      surface: '이해하기',
      morphs: [
        { lex: '이해', tag: 'NNG' },
        { lex: '하', tag: 'XSV' },
        { lex: '기', tag: 'ETN' },
      ],
      word: '이해하기',
      vocabulary: '이해',
    },
    {
      surface: '쉽어요.',
      morphs: [
        { lex: '쉽', tag: 'VA' },
        { lex: '어요', tag: 'EF' },
        { lex: '.', tag: 'SF' },
      ],
      word: '쉬워요.',
      vocabulary: '쉽다',
    },
    { surface: '매일', morphs: [{ lex: '매일', tag: 'MAG' }], word: '매일', vocabulary: '매일' },
    {
      surface: '조금씩',
      morphs: [
        { lex: '조금', tag: 'NNG' },
        { lex: '씩', tag: 'XSN' },
      ],
      word: '조금씩',
      vocabulary: '조금',
    },
    {
      surface: '실력이',
      morphs: [
        { lex: '실력', tag: 'NNG' },
        { lex: '이', tag: 'JKS' },
      ],
      word: '실력이',
      vocabulary: '실력',
    },
    {
      surface: '늘는',
      morphs: [
        { lex: '늘', tag: 'VV' },
        { lex: '는', tag: 'ETM' },
      ],
      word: '느는',
      vocabulary: '늘다',
    },
    {
      surface: '것이',
      morphs: [
        { lex: '것', tag: 'NNB' },
        { lex: '이', tag: 'JKS' },
      ],
      word: '게',
      vocabulary: '것',
    },
    {
      surface: '느끼어지어요!!',
      morphs: [
        { lex: '느끼', tag: 'VV' },
        { lex: '어', tag: 'EC' },
        { lex: '지', tag: 'VX' },
        { lex: '어요', tag: 'EF' },
        { lex: '!!', tag: 'SE' },
      ],
      word: '느껴져요!!',
      vocabulary: '느끼다',
    },
    {
      surface: '공부가',
      morphs: [
        { lex: '공부', tag: 'NNG' },
        { lex: '가', tag: 'JKS' },
      ],
      word: '공부가',
      vocabulary: '공부',
    },
    {
      surface: '놀이처럼',
      morphs: [
        { lex: '놀이', tag: 'NNG' },
        { lex: '처럼', tag: 'JKB' },
      ],
      word: '놀이처럼',
      vocabulary: '놀이',
    },
    {
      surface: '바뀌ㄴ',
      morphs: [
        { lex: '바뀌', tag: 'VV' },
        { lex: 'ㄴ', tag: 'ETM' },
      ],
      word: '바뀐',
      vocabulary: '바뀌다',
    },
    { surface: '것', morphs: [{ lex: '것', tag: 'NNB' }], word: '것', vocabulary: '것' },
    {
      surface: '같아요!',
      morphs: [
        { lex: '같', tag: 'VA' },
        { lex: '아요', tag: 'EF' },
        { lex: '!', tag: 'SF' },
      ],
      word: '같아요!',
      vocabulary: '같다',
    },
  ],
  vocab: [
    {
      id: 28283,
      written: '안녕',
      category: 'noun',
      senses: [
        {
          id: 39249,
          translation: 'peace; good health',
          definition: 'The state of being comfortable with no worry nor problem.',
        },
      ],
    },
    {
      id: 28284,
      written: '안녕',
      category: 'Interjection',
      senses: [
        {
          id: 39250,
          translation: 'hello; hi; good-bye; bye',
          definition:
            'A salutation uttered when the speaker meets or parts from his/her friend or junior.',
        },
      ],
    },
    {
      id: 36487,
      written: '저',
      category: 'pronoun',
      senses: [
        {
          id: 50516,
          translation: 'I; me',
          definition:
            'The humble form used by the speaker to refer to himself/herself for the purpose of showing humility to the listener.',
        },
      ],
    },
    {
      id: 36489,
      written: '저',
      category: 'pronoun',
      senses: [
        {
          id: 50518,
          translation: 'he; she',
          definition: 'A word used to indicate a person who is being talked about.',
        },
      ],
    },
    {
      id: 36491,
      written: '저',
      category: 'pronoun',
      senses: [
        {
          id: 50520,
          translation: 'that',
          definition:
            'A word used to indicate something that is far away from the speaker and the listener.',
        },
        { id: 50521, translation: 'that', definition: "A word that means 'that person.'" },
      ],
    },
    {
      id: 36492,
      written: '저',
      category: 'determiner',
      senses: [
        {
          id: 50522,
          translation: 'that',
          definition:
            'A word used to indicate a person who is far away from the speaker and the listener.',
        },
      ],
    },
    {
      id: 36493,
      written: '저',
      category: 'Interjection',
      senses: [
        {
          id: 50523,
          translation: 'um; uh; erm',
          definition: 'An exclamation used when one cannot immediately think of anything to say.',
        },
        {
          id: 50524,
          translation: 'um; uh; erm',
          definition:
            'An exclamation used when one is hesitant since he/she finds it hard to bring up something.',
        },
      ],
    },
    {
      id: 36494,
      written: '저',
      category: 'noun',
      senses: [
        {
          id: 50525,
          translation: 'author; be authored; be written',
          definition: "A word meaning 'written' or 'authored'.",
        },
      ],
    },
    {
      id: 31718,
      written: '요즘',
      category: 'noun',
      senses: [
        {
          id: 44106,
          translation: 'nowadays; these days',
          definition: 'A period from a while ago to the present. ',
        },
      ],
    },
    {
      id: 46939,
      written: '한국어',
      category: 'noun',
      senses: [
        {
          id: 65114,
          translation: 'Korean; Korean language',
          definition: 'The language used by the Korean people.',
        },
      ],
    },
    {
      id: 30381,
      written: '열심히',
      category: 'adverb',
      senses: [
        {
          id: 42245,
          translation: 'hard; diligently; zealously',
          definition: "With all one's heart.",
        },
      ],
    },
    {
      id: 3988,
      written: '공부',
      category: 'noun',
      senses: [
        {
          id: 5334,
          translation: 'study',
          definition: 'The act of gaining knowledge by learning studies or techniques.',
        },
      ],
    },
    {
      id: 35217,
      written: '있다',
      category: 'verb',
      senses: [
        {
          id: 48727,
          translation: 'be; stay',
          definition:
            'For a person or animal to remain in a certain place without leaving or getting out of it.',
        },
        { id: 48728, translation: 'work for; serve', definition: 'To keep working for a company.' },
        {
          id: 48729,
          translation: 'keep',
          definition: 'For a person or animal to maintain a certain state.',
        },
        {
          id: 48730,
          translation: '(no equivalent expression)',
          definition: 'For some time to pass.',
        },
      ],
    },
    {
      id: 35218,
      written: '있다',
      category: 'adjective',
      senses: [
        {
          id: 48731,
          translation: 'existent; existing',
          definition: 'A person, an animal, an object, etc., being in existence.',
        },
        {
          id: 48732,
          translation: '(no equivalent expression)',
          definition: 'A fact or a phenomenon being existent.',
        },
        {
          id: 48733,
          translation: '(no equivalent expression)',
          definition: 'Something being planned to be realized or happen.',
        },
        {
          id: 48734,
          translation: 'rich; wealthy',
          definition: 'Having enough or a lot of property.',
        },
        { id: 48735, translation: 'able to', definition: 'Having an ability to do something.' },
        {
          id: 48736,
          translation: '(no equivalent expression)',
          definition: 'The possibility of something happening or something actually happening.',
        },
        {
          id: 48737,
          translation: '(no equivalent expression)',
          definition: 'A word used when emphasizing or confirming a certain object or fact.',
        },
        {
          id: 48738,
          translation: '(no equivalent expression)',
          definition: 'Something occupying a certain place or space and existing there.',
        },
        {
          id: 48739,
          translation: '(no equivalent expression)',
          definition: 'A person or animal staying or living in a certain place.',
        },
        {
          id: 48740,
          translation: '(no equivalent expression)',
          definition: 'A person working for a certain company.',
        },
        {
          id: 48741,
          translation: '(no equivalent expression)',
          definition: 'Being in a certain situation, level, stage, etc.',
        },
        {
          id: 48742,
          translation: '(no equivalent expression)',
          definition: 'A person, object, etc., being included in something.',
        },
        {
          id: 48743,
          translation: '(no equivalent expression)',
          definition: 'Having a certain object, qualification, ability, etc.',
        },
        {
          id: 48744,
          translation: '(no equivalent expression)',
          definition: 'Having a person with whom one has a certain relation.',
        },
        {
          id: 48745,
          translation: '(no equivalent expression)',
          definition: 'Something happening to someone.',
        },
        {
          id: 48746,
          translation: '(no equivalent expression)',
          definition:
            'A word used when having the preceding noun as the subject of conversation or discussion.',
        },
        {
          id: 48747,
          translation: '(no equivalent expression)',
          definition: 'A person being in a certain social status or playing a certain role.',
        },
        {
          id: 48748,
          translation: '(no equivalent expression)',
          definition: 'A reason, possibility, etc., being established.',
        },
      ],
    },
    {
      id: 35219,
      written: '있다',
      category: 'auxiliary verb',
      senses: [
        {
          id: 48749,
          translation: 'itda',
          definition:
            'An auxiliary verb used to indicate the continuation of the state of the preceding statement.',
        },
        {
          id: 48750,
          translation: 'itda',
          definition:
            'An auxiliary verb used to indicate the continuation of the action of the preceding statement.',
        },
        {
          id: 48751,
          translation: 'itda',
          definition:
            'An auxiliary verb used to indicate the continuation of the result of the action of the preceding statement.',
        },
      ],
    },
    {
      id: 11579,
      written: '덕분',
      category: 'noun',
      senses: [
        {
          id: 16040,
          translation: 'indebtedness',
          definition: 'Grace or help given by someone; or the benefit of something happening.',
        },
      ],
    },
    {
      id: 49373,
      written: '훨씬',
      category: 'adverb',
      senses: [
        {
          id: 68404,
          translation: 'by far; much; a lot',
          definition:
            'In the state of something being greatly different from something else it is being compared to.',
        },
      ],
    },
    {
      id: 39615,
      written: '즐겁다',
      category: 'adjective',
      senses: [
        {
          id: 54675,
          translation: 'joyful; pleasant',
          definition: 'Pleased and satisfied with something.',
        },
      ],
    },
    {
      id: 29169,
      written: '어렵다',
      category: 'adjective',
      senses: [
        {
          id: 40479,
          translation: 'difficult; challenging',
          definition: 'Very complicated or hard to do.',
        },
        {
          id: 40480,
          translation: 'difficult; hard',
          definition: 'Being in serious trouble or suffering great hardship.',
        },
        {
          id: 40481,
          translation: 'difficult',
          definition: 'Not easy to understand some words or a piece of writing.',
        },
        {
          id: 40482,
          translation: 'difficult',
          definition: 'Hard to make a living because one is poor.',
        },
        {
          id: 40483,
          translation: 'difficult',
          definition: 'Fastidious and not well-rounded in personality.',
        },
        { id: 40484, translation: 'difficult', definition: 'Low in possibility.' },
        {
          id: 40485,
          translation: 'difficult',
          definition: 'Awkward and cautious because one feels distant to someone else.',
        },
      ],
    },
    {
      id: 10549,
      written: '단어',
      category: 'noun',
      senses: [
        {
          id: 14657,
          translation: 'word',
          definition:
            'The smallest independent unit of language, which has a certain meaning or function.',
        },
      ],
    },
    {
      id: 19730,
      written: '보다',
      category: 'verb',
      senses: [
        {
          id: 27717,
          translation: 'see; look at; notice',
          definition: 'To perceive with eyes the existence or appearance of an object.',
        },
        {
          id: 27718,
          translation: 'watch; see; enjoy',
          definition: 'To enjoy or appreciate an object with eyes.',
        },
        {
          id: 27719,
          translation: 'read; look at; take a look at',
          definition:
            'To read and understand the words, pictures and symbols in a book, newspaper, map, etc.',
        },
        {
          id: 27720,
          translation: 'look at; take a look at; look in',
          definition: 'To inspect an object to understand its content or state.',
        },
        { id: 27721, translation: 'meet; see', definition: 'To meet a person for a purpose.' },
        {
          id: 27722,
          translation: 'take care of; look after; guard',
          definition: 'To watch out for or take care of something.',
        },
        {
          id: 27723,
          translation: 'look at; assess; judge from',
          definition: 'To perceive and assess an incident or situation.',
        },
        {
          id: 27724,
          translation: 'have told',
          definition: 'To try to predict the future or fate by fortune-telling and etc.',
        },
        {
          id: 27725,
          translation: 'take',
          definition: "To take a test to assess one's knowledge or ability.",
        },
        {
          id: 27726,
          translation: 'work on; work; take care of; do business',
          definition: 'To work on or handle a task.',
        },
        {
          id: 27727,
          translation: 'achieve; reach; get to',
          definition: 'To achieve certain results.',
        },
        {
          id: 27728,
          translation: 'prepare; fix; make',
          definition: 'To prepare a dining table, spleeping place, etc.',
        },
        {
          id: 27729,
          translation: 'relieve, do',
          definition: '(euphemism) To defecate or urinate.',
        },
        { id: 27730, translation: 'have', definition: 'To have as a new family member.' },
        {
          id: 27731,
          translation: 'suffer; experiecne; gain; make',
          definition: 'To suffer, experience or gain something.',
        },
        {
          id: 27732,
          translation: 'examine; see',
          definition: 'For a doctor to examine a patient.',
        },
        {
          id: 27733,
          translation: 'subscribe to',
          definition: 'To receive and read a newspaper or magazine regularly.',
        },
        {
          id: 27734,
          translation: 'taste; sample',
          definition: 'To eat a small amount to distinguish a flavor.',
        },
        {
          id: 27735,
          translation: 'badmouth; speak ill of',
          definition: "To reveal and talk about somone else's shortcomings, etc.",
        },
        {
          id: 27736,
          translation: 'notice; recognize; see',
          definition: "To notice someone else's shortcomings or weaknesses.",
        },
        {
          id: 27737,
          translation: 'wait for; await; look for',
          definition: "To see if it's the right opportunity, moment or time.",
        },
        {
          id: 27738,
          translation: 'see; take a look at',
          definition: 'To take a careful look at something before deciding to buy it.',
        },
        {
          id: 27739,
          translation: 'purchase; buy; get',
          definition: 'To purchase something at a market.',
        },
        { id: 27740, translation: 'judge from', definition: 'To judge based on evidence.' },
        { id: 27741, translation: 'see', definition: "To direct one's action towards something." },
        {
          id: 27742,
          translation: 'take into account; consider',
          definition: "To take into account someone else's situation.",
        },
        {
          id: 27743,
          translation: 'depend on; rely on; count on',
          definition: 'To desire or depend on.',
        },
        { id: 27744, translation: 'meet; see', definition: 'To meet a person.' },
        {
          id: 27745,
          translation: 'attend; go to',
          definition: 'To attend a service at a Christian church.',
        },
        {
          id: 27746,
          translation: 'think of; see; regard; consider',
          definition: 'To evaluate or assess.',
        },
      ],
    },
    {
      id: 19731,
      written: '보다',
      category: 'auxiliary verb',
      senses: [
        {
          id: 27747,
          translation: 'try',
          definition:
            'An auxiliary verb used to indicate testing to do an action in the preceding statement.',
        },
        {
          id: 27748,
          translation: 'experience',
          definition:
            'An auxiliary verb used when one has already experienced an action in the preceding statement.',
        },
        {
          id: 27749,
          translation: 'boda',
          definition:
            'An auxiliary verb indicating when one first does an action meaning the preceding statement and thinks of its consequence later.',
        },
        {
          id: 27750,
          translation: 'boda',
          definition:
            'An auxiliary verb used when one realizes a fact anew in the following statement, or becomes a state in the following statement after doing an action in the preceding statement.',
        },
        {
          id: 27751,
          translation: 'boda',
          definition:
            'An auxiliary verb used when one realizes a fact anew in the following statement, or becomes a state in the following statement while doing an action in the preceding statement.',
        },
      ],
    },
    {
      id: 19732,
      written: '보다',
      category: 'auxiliary adjective',
      senses: [
        {
          id: 27752,
          translation: 'boda',
          definition:
            'An auxiliary adjective used to indicate that the act or state mentioned in the preceding statement is guessed by or is known to the speaker, though not precisely.',
        },
        {
          id: 27753,
          translation: 'boda',
          definition:
            'An auxiliary adjective used to indicate that the speaker has an intention to do the act mentioned in the preceding statement.',
        },
        {
          id: 27754,
          translation: 'boda',
          definition:
            'An auxiliary adjective used to indicate that the speaker is worried or afraid that the situation mentioned in the preceding statement may happen.',
        },
        {
          id: 27755,
          translation: 'than',
          definition:
            'A word that indicates that the situation or state referred to by the preceding word has priority over others.',
        },
        {
          id: 27756,
          translation: 'boda',
          definition:
            'An auxiliary adjective used to indicate that the state mentioned in the preceding statement is a cause for the following statement.',
        },
      ],
    },
    {
      id: 19733,
      written: '보다',
      category: 'adverb',
      senses: [
        { id: 27757, translation: 'more', definition: 'More than, when compared to something. ' },
      ],
    },
    {
      id: 19734,
      written: '보다',
      category: 'postpositional particle',
      senses: [
        {
          id: 27758,
          translation: 'boda',
          definition:
            'A postpositional particle that indicates the subject of a comparison when comparing different things.',
        },
      ],
    },
    {
      id: 26313,
      written: '쉽다',
      category: 'adjective',
      senses: [
        { id: 36539, translation: 'easy', definition: 'Not hard or difficult to do.' },
        { id: 36540, translation: 'easy; common', definition: 'Not hard to encounter or witness.' },
        { id: 36541, translation: 'easy; prone', definition: 'Having a lot of possibility.' },
      ],
    },
    {
      id: 37636,
      written: '정리',
      category: 'noun',
      senses: [
        {
          id: 51994,
          translation: 'organizing',
          definition: 'The act of gathering or clearing away dispersed or unorganized items.',
        },
        {
          id: 51995,
          translation: 'putting together',
          definition: 'The act of categorizing or gathering systematically.',
        },
        {
          id: 51996,
          translation: 'removal; redevelopment',
          definition:
            'The act of establishing a certain order by reducing or clearing away something problematic or unnecessary.',
        },
        {
          id: 51997,
          translation: 'end',
          definition: 'The act of ending a relationship with another person.',
        },
        {
          id: 51998,
          translation: 'update',
          definition:
            "The act of making the transaction history with a bank shown on one's passbook.",
        },
      ],
    },
    {
      id: 46957,
      written: '한눈',
      category: 'noun',
      senses: [
        {
          id: 65133,
          translation: 'one glance; one look',
          definition: 'An act of taking a look at something once or briefly.',
        },
        {
          id: 65134,
          translation: 'one glance; a single view',
          definition: "The range that one can see at a time with one's eyes.",
        },
      ],
    },
    {
      id: 13281,
      written: '들어오다',
      category: 'verb',
      senses: [
        {
          id: 18609,
          translation: 'come in; get in; enter',
          definition: 'To move inside from outside within a certain range.',
        },
        {
          id: 18610,
          translation: 'get; gain; earn',
          definition: 'To gain something such as income.',
        },
        {
          id: 18611,
          translation: 'come in; be transmitted; be introduced',
          definition: 'For thoughts, culture or technology to be transmitted from the outside in.',
        },
        {
          id: 18612,
          translation: 'be available; be made available; be supplied; be provided',
          definition: 'For facilities such as electricity or water supply to be built or provided.',
        },
        {
          id: 18613,
          translation: 'join',
          definition: 'To become a member of a certain group or organization.',
        },
        {
          id: 18614,
          translation: 'come in; enter',
          definition: 'To be included within a certain range or standard.',
        },
        {
          id: 18615,
          translation: 'come in; be acquired',
          definition:
            'For something to be given to or acquired by someone or a certain organization.',
        },
        {
          id: 18616,
          translation: "be understood; be comprehended; come into one's head",
          definition: 'For a certain content to be understood and remembered.',
        },
        {
          id: 18617,
          translation: 'be heard; be delivered; be sent; come in',
          definition: 'For news, rumor, demand, etc. to be heard or reported.',
        },
      ],
    },
    {
      id: 34357,
      written: '이해',
      category: 'noun',
      senses: [
        {
          id: 47580,
          translation: 'gains and losses; interests',
          definition: 'Gains and losses or benefit and harm. ',
        },
      ],
    },
    {
      id: 34358,
      written: '이해',
      category: 'noun',
      senses: [
        {
          id: 47581,
          translation: 'understanding; comprehension',
          definition:
            'The state of knowing what something is; the process of accepting something as something else.',
        },
        {
          id: 47582,
          translation: 'understanding',
          definition:
            'The state of having realized and knowing something; the process of knowing and accepting something.',
        },
        {
          id: 47583,
          translation: 'understanding',
          definition: "The process of knowing and accepting someone's situation or circumstances.",
        },
      ],
    },
    {
      id: 15069,
      written: '매일',
      category: 'noun',
      senses: [{ id: 21407, translation: 'everyday', definition: 'Every single day.' }],
    },
    {
      id: 15070,
      written: '매일',
      category: 'adverb',
      senses: [
        {
          id: 21408,
          translation: 'every day; every single day',
          definition: 'Every day without exceptions.',
        },
      ],
    },
    {
      id: 38228,
      written: '조금',
      category: 'noun',
      senses: [
        { id: 52762, translation: 'a little; little', definition: 'A small quantity or degree.' },
        { id: 52763, translation: 'a while', definition: 'A duration of short time.' },
      ],
    },
    {
      id: 38229,
      written: '조금',
      category: 'adverb',
      senses: [
        {
          id: 52764,
          translation: 'a little',
          definition: 'In a small quantity or to a small degree.',
        },
        { id: 52765, translation: 'a little', definition: 'For a short while.' },
      ],
    },
    {
      id: 27288,
      written: '실력',
      category: 'noun',
      senses: [
        {
          id: 37798,
          translation: 'ability; capability',
          definition: "One's ability to achieve something. ",
        },
        {
          id: 37799,
          translation: 'force; strong measure; strong action',
          definition: 'Physical or military force; or the force to make another do something.',
        },
      ],
    },
    {
      id: 10052,
      written: '늘다',
      category: 'verb',
      senses: [
        {
          id: 13919,
          translation: 'be extended',
          definition:
            'For the length, area, volume, etc., of something to become longer or bigger than before.',
        },
        {
          id: 13920,
          translation: 'multiply; grow',
          definition: 'For numbers, quantities, etc., to become greater than before.',
        },
        {
          id: 13921,
          translation: 'increase; rise',
          definition: 'For power, energy, force, etc., to become stronger than before.',
        },
        {
          id: 13922,
          translation: 'improve; make progress',
          definition: "To become better at something as one's talent, ability, etc., improves.",
        },
        {
          id: 13923,
          translation: 'increase; improve',
          definition: "For one's fortune to improve.",
        },
        {
          id: 13924,
          translation: 'be extended',
          definition: 'For time or a period to become longer.',
        },
      ],
    },
    {
      id: 2189,
      written: '것',
      category: 'dependent noun',
      senses: [
        {
          id: 3074,
          translation: 'something',
          definition:
            'A bound noun used to refer to a thing or fact that is not specified or determind by someone.',
        },
        {
          id: 3075,
          translation: '(no equivalent expression)',
          definition: '(disparaging) A bound noun used to refer to a person or animal.',
        },
        {
          id: 3076,
          translation: '(no equivalent expression)',
          definition: 'A bound noun used to indicate that something belongs to a certain person.',
        },
        {
          id: 3077,
          translation: '(no equivalent expression)',
          definition: 'A bound noun used to indicate a certain act, situation, or accomplishment.',
        },
        {
          id: 3078,
          translation: '(no equivalent expression)',
          definition:
            "A bound noun used to indicate one's confidence or emphasis regarding a certain fact.",
        },
        {
          id: 3079,
          translation: '(no equivalent expression)',
          definition:
            "A bound noun used to indicate one's prediction, guess, and plan regarding a thing that has not occurred yet.",
        },
        {
          id: 3080,
          translation: '(no equivalent expression)',
          definition:
            'A sentence-concluding bound noun carrying the sense of a command or instruction.',
        },
      ],
    },
    {
      id: 9965,
      written: '느끼다',
      category: 'verb',
      senses: [
        {
          id: 13790,
          translation: 'sob; blubber; whimper',
          definition: "To cry sorrowfully while gulping down one's tears.",
        },
        { id: 13791, translation: 'be out of breath; pant', definition: 'To gasp for breath.' },
      ],
    },
    {
      id: 9966,
      written: '느끼다',
      category: 'verb',
      senses: [
        {
          id: 13792,
          translation: 'feel',
          definition:
            'To perceive a certain stimulus through a sensory organ such as the nose, skin, etc.',
        },
        {
          id: 13793,
          translation: 'feel',
          definition: "To experience a certain emotion in one's mind.",
        },
        {
          id: 13794,
          translation: 'realize; become aware of',
          definition: "To know a certain truth by realizing it in one's mind.",
        },
        {
          id: 13795,
          translation: 'think',
          definition: 'To think about or perceive a certain subject or situation in a certain way.',
        },
        {
          id: 13796,
          translation: 'experience; know',
          definition: 'To experience something in person and understand it.',
        },
      ],
    },
    {
      id: 9586,
      written: '놀이',
      category: 'noun',
      senses: [
        {
          id: 13242,
          translation: 'play; entertainment',
          definition: 'The act of enjoying something or playing for fun. ',
        },
        {
          id: 13243,
          translation: 'play; entertainment; performance',
          definition:
            'A traditional Korean entertainment or performance played by a number of people according to a certain rule, on a festive day or special occasion.',
        },
        {
          id: 13244,
          translation: 'game',
          definition: 'The act of playing a game according to a certain rule or method. ',
        },
        {
          id: 13245,
          translation: 'play',
          definition: "The word meaning 'acting in jest' or 'mimicking' something.",
        },
      ],
    },
    {
      id: 17483,
      written: '바뀌다',
      category: 'verb',
      senses: [
        {
          id: 24624,
          translation: 'be changed; be replaced',
          definition: 'For something that has existed to be replaced by something else.',
        },
        {
          id: 24625,
          translation: 'be translated',
          definition: 'For a language to be translated into another language.',
        },
        {
          id: 24626,
          translation: 'be changed; be exchanged',
          definition:
            "To have one's own object taken by someone and to take his/her object instead.",
        },
        {
          id: 24627,
          translation: 'become different',
          definition: 'For a content, state, etc., to become changed or different.',
        },
        {
          id: 24628,
          translation: 'turn',
          definition: 'To become the next day, month, year, season, etc., as time goes by.',
        },
        { id: 24629, translation: 'become the next turn', definition: 'To become the next turn.' },
      ],
    },
    {
      id: 1271,
      written: '같다',
      category: 'adjective',
      senses: [
        {
          id: 1796,
          translation: 'same; identical; equal',
          definition: 'Not different from each other.',
        },
        { id: 1797, translation: 'similar; like', definition: 'Similar to each other.' },
        {
          id: 1798,
          translation: 'such as; like',
          definition:
            'A term used to indicate that one is classified into a similar group with something.',
        },
        {
          id: 1799,
          translation: 'if; in case',
          definition: 'A term used to indicate &apos;under a certain situation or condition&apos;.',
        },
        {
          id: 1800,
          translation: '(no equivalent expression)',
          definition: 'A term used to indciate &apos;meeting a standard&apos;.',
        },
        {
          id: 1801,
          translation: '(no equivalent expression)',
          definition:
            'A term meaning &apos;according to one&apos;s mind, thought, situation, etc.&apos;,  used to indicate that the reality is the opposite.',
        },
        {
          id: 1802,
          translation: 'just like',
          definition:
            '(insulting) A term used to indicate that something is not different from what is being referred to.',
        },
        {
          id: 1803,
          translation: '(no equivalent expression)',
          definition: 'Being a fact that one can guess.',
        },
      ],
    },
  ],
}
