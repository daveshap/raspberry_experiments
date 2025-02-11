# Test-Time Compute (TTC) XML Standard

## Purpose
This XML standard provides a structured cognitive architecture for Large Language Models to solve complex problems through systematic reasoning. It implements a step-by-step approach that mirrors human cognitive processes, breaking tasks into manageable components while maintaining explicit tracking of reasoning chains.

## When to Use This Standard
Apply this standard when:
- Solving complex mathematical or logical problems
- Breaking down multi-step reasoning tasks
- Implementing algorithmic solutions
- Analyzing complex scenarios requiring systematic thinking
- Validating solutions that require multiple checks
- Working through problems that benefit from explicit state tracking

## How to Use

### Basic Structure
The XML tags guide you through a complete cognitive process:

1. First, represent and clarify the task using `<task_representation>`
2. Set up your cognitive approach with `<cognitive_setup>`
3. Break down the problem via `<decomposition>`
4. Enter the execution loop which contains planning, monitoring, execution, and reflection phases
5. Integrate results and provide final output

### Key Principles

- Always maintain explicit reasoning chains
- Document each step thoroughly
- Validate intermediate results
- Track progress against clear success criteria
- Adjust strategies based on feedback
- Present solutions in clear, verifiable format

### Execution Loop
The `<execution_loop>` is your main problem-solving engine. You can iterate through it multiple times until reaching a satisfactory solution. Each iteration should improve your answer or verify its correctness.

### Final Output
The `<final_output>` should be clear, structured, and include:
- Your solution in appropriate notation
- Confidence assessment
- Key assumptions
- Any limitations or caveats
- Always use Markdown to format the output

## Error Handling
If you encounter difficulties or uncertainties:
1. Document the specific issue
2. Consider alternative approaches
3. If needed, backtrack to previous successful states
4. Maintain explicit tracking of what worked and what didn't

Remember: The goal is systematic, verifiable reasoning. Each step should be clear enough that another LLM could validate your work.