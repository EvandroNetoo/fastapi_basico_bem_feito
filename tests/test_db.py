from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.models import User


def test_create_user(session: Session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.id == 1
