# Commands

## Raw
```powershell
stubgen src/chriscarl -o dist/typing
stubgen -m logging -o dist/typing
stubgen -m logging.handles -o dist/typing
pytest --cov=chriscarl tests --cov-report term-missing
pytest --cov=chriscarl.core.types tests/chriscarl/core/types --cov-report term-missing
```

## dev
```powershell
dev audit cov --module chriscarl.core.types --tests-dirname tests/chriscarl/core/types
```