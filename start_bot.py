#!/usr/bin/env python3
"""
Safe bot launcher with process checking.
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path


def check_running_processes():
    """Check if bot is already running."""
    try:
        # Check for running bot processes
        result = subprocess.run(
            ["pgrep", "-f", "python.*main.py"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            return [pid for pid in pids if pid]
        
        return []
    except Exception:
        return []


def kill_existing_processes():
    """Kill existing bot processes."""
    processes = check_running_processes()
    
    if processes:
        print(f"🔄 Найдено {len(processes)} запущенных процессов бота")
        print("⏹️  Останавливаю существующие процессы...")
        
        try:
            subprocess.run(["pkill", "-f", "python.*main.py"], check=False)
            time.sleep(3)  # Wait for processes to stop
            
            # Check again
            remaining = check_running_processes()
            if remaining:
                print("⚠️  Принудительно завершаю оставшиеся процессы...")
                subprocess.run(["pkill", "-9", "-f", "python.*main.py"], check=False)
                time.sleep(2)
                
        except Exception as e:
            print(f"❌ Ошибка при остановке процессов: {e}")
            return False
            
        print("✅ Все процессы остановлены")
    
    return True


def check_dependencies():
    """Check if all dependencies are installed."""
    try:
        import aiogram
        import sqlalchemy
        import pydantic
        import pydantic_settings
        return True
    except ImportError as e:
        print(f"❌ Отсутствует зависимость: {e}")
        print("📦 Установите зависимости: pip install -r requirements.txt")
        return False


def main():
    """Main launcher function."""
    print("🚀 NOFACE.digital Bot Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Kill existing processes
    if not kill_existing_processes():
        print("❌ Не удалось остановить существующие процессы")
        sys.exit(1)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🏁 Запускаю бота...")
    print("📝 Для остановки нажмите Ctrl+C")
    print("-" * 40)
    
    try:
        # Run the bot
        subprocess.run([sys.executable, "main.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n⏹️  Бот остановлен пользователем")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Бот завершился с ошибкой: {e}")
        sys.exit(e.returncode)
        
    except Exception as e:
        print(f"\n💥 Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 