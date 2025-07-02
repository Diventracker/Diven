from usuarios.model import Usuario


class UsuarioCRUD:
    def __init__(self, repo):
        self.repo = repo

    def listar_todos(self) -> list[Usuario]:
        return self.repo.listar_todos()
