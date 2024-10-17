# Foodie Dash (client)
Client version of the foodie dash

# Information
## Compile Command
We use Nuitka to compile the executable

Here is the command we use:
```
python3 -m nuitka --onefile --standalone --windows-icon-from-ico=foodie-dash.ico --windows-console-mode=disable --enable-plugin=tk-inter  --output-filename=Foodie-Dash compiled_client.py
```

## Files
File compiled by Nuitka: [compiled_client.py](https://github.com/Lncvrt/Foodie-Archive/blob/client/compiled_client.py)

File the compiled client calls: [client.py](https://github.com/Lncvrt/Foodie-Archive/blob/client/client.py)
