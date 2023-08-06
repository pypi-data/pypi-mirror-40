<p align="center">
    <img src="https://min.gitcdn.link/repo/tanrax/get-my-pastebin/master/logo.png">
</p>

Terminal application to find and copy your own Paste for Pastebin.

- Search in Paste public and private state.
- Copies to the clipboard raw Paste automatically.
- Prints raw Paste by console.

<p align="center">
    <img src="https://min.gitcdn.link/cdn/tanrax/get-my-pastebin/master/demo.svg">
</p>

## Use

``` bash
getmypastebin --api-key [Get Developer API Key] --username [username account Pastebin] --password [password account Pastebin] [search]
```

[Get Developer API Key](https://pastebin.com/api#1)

Example

``` bash
getmypastebin --api-key 123qwe456rty --username example --password 123 wordpress
```

## Install

``` bash
pip3 install --user get-my-pastebin 
```

## Update

``` bash
pip3 install --user --upgrade get-my-pastebin
```

## Alias

Optimize with alias in your `.bashrc` or `.zshrc`.

``` bash
alias gpaste='getmypastebin --api-key 123qwe456rty --username example --password 123'
```

Use.

``` bash
gpaste python
```

