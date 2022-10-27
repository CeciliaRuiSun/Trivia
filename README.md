# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game. The application function includes:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## APIs
GET `'/categories'`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key: value pairs.
- Example:
```bash
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

GET `'/questions'`
- Fetches all questions in database
- Request Arguments: None
- Returns: A list of questions with id, question content, answer, category and question difficulty level.
- Example:
```bash
"questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
]
```

DELETE `'/questions/<int:question_id>'`
- Delete a specific question whose id equals `question_id`
- Request Arguments: `question_id`
- Returns: The updated list of questions after deletion
- Example:
```bash
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
```

POST `'/questions'`
- Add a new question
- Request Arguments: `{id: int, question: String, answer: String, category: string, difficulty: int}`
- Returns: A list of updated questions with id, question content, answer, category and question difficulty level.
- Example:
```bash
"questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
]
```

POST `'/questions/search'`
- Fetches all questions whose question content contains seach item
- Request Arguments: `{Search: String}`
- Returns: The list of questions 

GET `'/category/<int:category_id>/questions'`
- Fetches questions in the given category
- Request Arguments:`category_id`
- Returns: The list of questions within the category

POST `'/quiz'`
- Fetches questions in the given category and not in previous questions
- Request Arguments: `category_id`, `pre_questions:[]`
- Returns: A list of questions.

