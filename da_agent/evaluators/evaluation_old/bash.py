       
       
def bash_check(bash_path: str, env) -> float:
    with open(bash_path, 'r') as file:
        bash_code = file.read()

    obs = env.execute_code(bash_code)
    # if 'succeed' in obs:
    #     score = 1
    # else:
    #     score = 0
    
    
    return score