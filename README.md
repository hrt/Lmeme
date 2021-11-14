# League of Legends Orbwalker

[![Alt text](https://img.youtube.com/vi/TBaV1QA_NBk/0.jpg)](https://www.youtube.com/watch?v=TBaV1QA_NBk)

## Usage
1. Install python3
2. Create a python3 venv
3. Install the requirements `pip install -r requirements.txt`
4. Get in game and run `main.py`
5. Hold down space to attack champions

Note that this repo currently assumes that you have "Target Champions Only" binded to middle mouse (MB3)

## Offsets
I've only ever wrote this for a single patch of league of legends (11.2.1) so it's hard to say if the signatures I've come up with will work in the future. They were found using IDA.


| Name                  | Signature                                                                                     								| Extra Note        |
| :---                  |    :----:                                                                                     								|          ---:     |
| `oLocalPlayer`        | `\x8B\x3D\x00\x00\x00\x00\x3B\xF7\x75 xx????xxx`                                              								| aBlueHero (string)|
| `oObjectManager`      | `\x8B\x0D\x00\x00\x00\x00\x89\x7C\x24\x14 xx????xxxx`                                         								|       -           |
| `oObjectManager`      | `\x8B\x0D\x00\x00\x00\x00\x56\x50\xE8\x00\x00\x00\x00\x8B\xF0 xx????xxx????xx`                								|       -           |
| `oViewProjMatrices`   | `\xB9\x00\x00\x00\x00\x0F\x10\x80 x????xxx`                                                   								|       -           |
| `oViewProjMatrices`   | `\x68\x00\x00\x00\x00\x51\x8B\x00 x????xxx`                                                   								|       -           |
| `oViewProjMatrices`   | `\x68\x00\x00\x00\x00\x8D\x84\x24\x00\x00\x00\x00\x50\x8B\x44\x24\x1C x????xxx????xxxxx`      								|       -           |
| `oRenderer`           | `\xA1\x00\x00\x00\x00\x53\x8B\x1D\x00\x00\x00\x00\x56\x57\x8B\xF9 x????xxx????xxxx`           								| aWidth (string)   |
| `oGameTime`           | `\xF3\x0F\x5C\x0D\x00\x00\x00\x00\x0F\x2F\xC1\xF3 xxxx????xxxx`                               								|       -           |
| `oObjectSpellBook`    | `\x8D\x89\x00\x00\x00\x00\xE8\x00\x00\x00\x00\xE8\x00\x00\x00\x00\x5F\xB0\x01\x5E\xC2\x04\x00\x5F xx??????????????xxxxxxxx`   |       -           |