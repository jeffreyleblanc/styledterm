from invoke import task

@task(default=True)
def example(c):
    import os
    c.run(f"PYTHONPATH={os.environ.get('PWD')} python3 examples/example4.py", pty=True)
