SELECT
    target_answer.answer_id AS answer_id,
    question.word AS answer_word
FROM (
    SELECT
        answer_id,
        question_id
    FROM answer
    WHERE audio_file_object_key = :object_key
) AS target_answer
JOIN question
USING (question_id);
