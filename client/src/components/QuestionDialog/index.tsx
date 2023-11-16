type Props = {
  content: string;
};

export default function QuestionDialog({ content }: Props) {
  return <dialog className="questionDialog">{content}</dialog>;
}
