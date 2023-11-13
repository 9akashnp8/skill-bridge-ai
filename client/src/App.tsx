import { useState, useEffect } from 'react'

type Question = {
  _id: string,
  topic: string,
  question: string
}

function App() {
  const [topic, setTopic] = useState<string>("");
  const [questions, setQuestions] = useState<Question[]>([])

  async function getTopicQuestions() {
    const result = await fetch('http://127.0.0.1:8000/practice/questions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        topic: 'slicing',
        options: {
          validate: false,
          re_gen: false,
          mock: true,
        }
      })
    })

    if (result.ok) {
      const response = await result.json()
      setQuestions(response)
    }
  }

  function pickRandomTopic() {
    setTopic('slicing')
  }

  useEffect(() => {
    pickRandomTopic()
    getTopicQuestions()
  }, [])

  function Questions() {
    return (
      <>
        <h2>Questions for Topic: {topic}</h2>
        {questions.map((question) => <p key={question._id}>{question.question}</p>)}
      </>
    )
  }

  return (
    <>
      <h1>Skill Bridge AI</h1>
      {topic ? <Questions /> : 'Question Pick Failed'}
    </>
  )
}

export default App
