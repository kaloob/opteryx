# Query Engine

## Flow

```mermaid
graph LR;
    Parser-->Lexer;
    Lexer-->Planner;
    Planner-->Optimizer;
    Optimizer-->Exectutor;
```