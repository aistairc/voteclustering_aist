package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"runtime"

	"github.com/fatih/color"
)

func commandAvailable(name string) bool {
	cmd := exec.Command(name, "--help")
	if err := cmd.Run(); err != nil {
		fmt.Println(err.Error())
		return false
	}
	return true
}

func showInstallation() {
	fmt.Println(`
docker-compose is required
See an official web site and install a package
https://docs.docker.com/get-docker/`)
}

func execCommandOnWindows(name string, arg ...string) {
	cmd := exec.Command(name, arg...)

	stdout, err := cmd.StdoutPipe()
	if err != nil {
		color.Red(err.Error())
		os.Exit(1)
	}

	stderr, err := cmd.StderrPipe()
	if err != nil {
		color.Red(err.Error())
		os.Exit(1)
	}

	streamReader := func(scanner *bufio.Scanner, oc chan string, dc chan bool) {
		defer close(oc)
		defer close(dc)
		for scanner.Scan() {
			oc <- scanner.Text()
		}
		dc <- true
	}

	stdoutScanner := bufio.NewScanner(stdout)
	stdoutOutputCh := make(chan string)
	stdoutDoneCh := make(chan bool)

	stderrScanner := bufio.NewScanner(stderr)
	stderrOutputCh := make(chan string)
	stderrDoneCh := make(chan bool)

	cmd.Start()

	go streamReader(stdoutScanner, stdoutOutputCh, stdoutDoneCh)
	go streamReader(stderrScanner, stderrOutputCh, stderrDoneCh)

	loop := true
	for loop {
		select {
		case <-stdoutDoneCh:
			loop = false
		case line := <-stdoutOutputCh:
			fmt.Println(line)
		case line := <-stderrOutputCh:
			fmt.Println(line)
		}
	}

	cmd.Wait()
}

func execCommand(name string, arg ...string) {
	// windows 用にビルドのときに有効化する
	if runtime.GOOS == "windows" {
		execCommandOnWindows(name, arg...)
	}

	// mac / linux 用にビルドのときに有効化する
	// cmd := exec.Command(name, arg...)
	// f, err := pty.Start(cmd)
	// if err != nil {
	// 	panic(err)
	// }
	// defer func() { f.Close() }()
	// io.Copy(os.Stdout, f)
}

func execStart(env string) {
	execCommand(
		"docker-compose",
		"-f", "docker-compose.yml",
		"-f", fmt.Sprintf("docker-compose.%s.yml", env),
		"up", "--build",
	)
}

func execStop() {
	execCommand(
		"docker-compose",
		"down",
	)
}

func execRestart() {
	execCommand(
		"docker-compose",
		"restart",
	)
}

func execDjangoMigrate() {
	execCommand(
		"docker-compose",
		"exec", "-T", "django",
		"python3", "manage.py", "migrate",
	)
}

func execDjangoSuperuser() {
	var username, email string
	color.Cyan("Create admin user to login to admin page")
	fmt.Printf("username: ")
	fmt.Scan(&username)
	fmt.Printf("email: ")
	fmt.Scan(&email)

	if len(username) <= 0 || len(email) <= 0 {
		color.Yellow("username and email are required to create admin")
		os.Exit(1)
	}

	execCommand(
		"docker-compose",
		"exec", "-T", "django",
		"python3", "manage.py", "createsu",
		"--username", username,
		"--email", email,
		"--password", "admin",
	)

	color.Green("Admin user was created and whose password was set as 'admin'")
	color.Red("!!!!! CHANGE THE PASSWORD on the admin site !!!!!")
}

func execDjangoCollectStatic() {
	execCommand(
		"docker-compose",
		"exec", "-T", "django",
		"python3", "manage.py", "collectstatic", "--noinput",
	)
}

func execLogs(container ...string) {
	if len(container) == 1 {
		execCommand(
			"docker-compose",
			"logs", "-f", "--tail=200", container[0],
		)
	}

	execCommand(
		"docker-compose",
		"logs", "-f", "--tail=200",
	)
}

func execDjangoMakeMessages() {
	execCommand(
		"docker-compose",
		"exec", "-T", "django",
		"python3", "manage.py", "makemessages", "-l", "en", "--no-location",
	)
}

func execDjangoCompileMessages() {
	execCommand(
		"docker-compose",
		"exec", "-T", "django",
		"python3", "manage.py", "compilemessages",
	)
}

func execGenerateERD() {
	execCommand(
		"docker-compose",
		"exec", "-T", "django",
		"python3", "manage_ERD/generate_ERD.py",
	)
}

func main() {
	cmd := flag.String("c", "", "Execution command: start, migrate, stop")
	env := flag.String("e", "development", "Environment name: development, production")
	flag.Parse()

	fmt.Printf("cmd: %s, env: %s\n", *cmd, *env)

	if ok := commandAvailable("docker-compose"); !ok {
		showInstallation()
		os.Exit(0)
	}

	switch *cmd {
	case "start":
		execStart(*env)
	case "stop":
		execStop()
	case "restart":
		execRestart()
	case "logdjango":
		execLogs("django")
	case "logall":
		execLogs()
	case "setup":
		execDjangoCollectStatic()
		execDjangoMigrate()
		execDjangoSuperuser()
	case "createsu":
		execDjangoSuperuser()
	case "migrate":
		execDjangoMigrate()
	case "collectstatic":
		execDjangoCollectStatic()
	case "makemessages":
		execDjangoMakeMessages()
	case "compilemessages":
		execDjangoCompileMessages()
	case "generateerd":
		execGenerateERD()
	default:
		c := color.New(color.FgRed)
		c.Printf("Unsupported arguments: %s\n", *cmd)
		flag.Usage()
	}
}
