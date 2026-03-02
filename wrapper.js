const { exec } = require('child_process');
const path = require('path');

// 财经分析工具包 - Node.js 包装器
class FinanceToolkitWrapper {
    constructor() {
        this.skillPath = path.join(process.env.USERPROFILE, '.openclaw', 'skills', 'finance-toolkit');
    }

    async runPython(script) {
        return new Promise((resolve, reject) => {
            exec(`python "${script}"`, { cwd: this.skillPath }, (error, stdout, stderr) => {
                if (error) {
                    reject(error);
                } else {
                    resolve(stdout || stderr);
                }
            });
        });
    }

    async getStockInfo(symbol) {
        const script = `
import sys
sys.path.insert(0, '${this.skillPath.replace(/\\/g, '\\\\')}')
from finance_toolkit import FinanceToolkit

toolkit = FinanceToolkit()
info = toolkit.get_stock_info('${symbol}')
if info:
    print(f"名称: {info['name']}")
    print(f"价格: ${info['current_price']:.2f}")
    print(f"涨跌: {info['change_percent']:.2f}%")
    print(f"市值: ${info['market_cap']:,.0f}")
    print(f"市盈率: {info['pe_ratio']:.2f}")
else:
    print("获取失败")
`;
        return await this.runPythonScript(script);
    }

    async runPythonScript(script) {
        return new Promise((resolve, reject) => {
            const { spawn } = require('child_process');
            const python = spawn('python', ['-c', script]);
            
            let output = '';
            python.stdout.on('data', (data) => {
                output += data.toString();
            });
            
            python.stderr.on('data', (data) => {
                output += data.toString();
            });
            
            python.on('close', (code) => {
                resolve(output);
            });
        });
    }
}

// 导出模块
module.exports = FinanceToolkitWrapper;

// 如果直接运行
if (require.main === module) {
    const toolkit = new FinanceToolkitWrapper();
    console.log('📈 财经分析工具包已加载');
    console.log('技能路径:', toolkit.skillPath);
}
