type Props = {
  question: string;
};

export default function QuestionCard({ question }: Props) {
  function handleClick() {
    const dialog = document.querySelector("dialog")!;
    dialog.innerHTML = question;
    dialog.showModal();
  }
  return (
    <p className="questionCard" onClick={handleClick}>
      {question}
    </p>
  );
}
