from app.memory import remember,recall
def test_persists_and_recalls(tmp_path):
    db=tmp_path/"test.db"; remember(db,"s1","User prefers concise technical examples",["preference"])
    result=recall(db,"concise technical examples")
    assert result and result[0]["session_id"]=="s1"
