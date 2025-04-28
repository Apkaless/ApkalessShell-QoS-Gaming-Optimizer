# QoS Manager for Gaming

A powerful Windows application for managing Quality of Service (QoS) policies to optimize gaming traffic and reduce latency.


## Features

### Game Management
- Auto-detect games from Steam and Epic Games
- Manual game addition with custom DSCP values
- Easy game removal and management
- Bulk DSCP value updates

### Performance Monitoring
- Real-time network performance metrics
- Latency, packet loss, and jitter monitoring
- Performance impact analysis
- Smart DSCP recommendations

### Advanced Diagnostics
- Network path analysis with traceroute
- Bandwidth testing (download/upload speeds)
- Bufferbloat detection
- Connection stability testing
- Detailed network interface information

### Optimization Tools
- Automatic DSCP value optimization
- Network performance recommendations
- Historical performance tracking
- Export performance data

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Apkaless/ApkalessShell-QoS-Gaming-Optimizer.git
cd ApkalessShell-QoS-Gaming-Optimizer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python QoS.py
```

## Requirements

- Windows 10 or later
- Python 3.7 or later
- Administrator privileges
- Network connection

## Dependencies

- ping3>=4.0.4
- speedtest-cli>=2.1.3

## Usage

### Adding Games
1. Use the "Add Game" tab to manually add games
2. Or use "Auto Detect" to find games from Steam/Epic
3. Set appropriate DSCP values (46 for highest priority)

### Performance Monitoring
1. Go to the "Performance" tab
2. Click "Start Performance Monitoring"
3. View real-time metrics and recommendations

### Network Diagnostics
1. Use the "Advanced Diagnostics" tab
2. Run bandwidth tests
3. Check for bufferbloat
4. Analyze connection stability

### DSCP Values Guide
- 46 (EF): Highest priority for competitive gaming
- 32 (CS4): High priority for casual gaming
- 24 (CS3): Medium priority for less demanding games

## Best Practices

### For Competitive Gaming
- Use DSCP 46 for all competitive games
- Monitor network performance regularly
- Use wired connection when possible
- Close bandwidth-intensive applications

### Network Setup
- Enable QoS on your router
- Use a gaming router with SQM if possible
- Keep network drivers updated
- Monitor for network congestion

## Troubleshooting

### Common Issues
1. **Application requires admin rights**
   - Run the application as administrator
   - Right-click the executable and select "Run as administrator"

2. **Games not detected**
   - Check if games are installed in default locations
   - Try manual game addition
   - Verify game executable paths

3. **Performance issues**
   - Check network diagnostics
   - Verify DSCP values
   - Monitor for network congestion

### Error Logs
- View error logs in the Settings tab
- Check the "Errors.txt" file in the application directory

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Windows QoS Policy Management
- Python Tkinter for GUI
- Speedtest-cli for bandwidth testing
- Ping3 for network latency testing

## Support

For support, please:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Contact the maintainers
