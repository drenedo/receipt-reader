import click
from ocr import scan
import time


@click.command()
@click.option("--image", required=True, help="Source path of the image")
@click.option("--margin", required=False, help="The margin applied for every step of the ocr process, "
                                               "by default 7 pixels")
@click.option("--line", required=False, help="The error in pixels to consider text is in the same line.")
@click.option("--model", required=False, help="TrOCR pretrained model. See https://huggingface.co/models?other=trocr "
                                              "for more models")
def ocr(image, margin, line, model):
    start_time = time.time()
    for oline in get_scan_results(image, margin, int(line) if line is not None else line, model):
        click.echo(oline.get_text())
    end_time = time.time()
    time_lapsed = end_time - start_time
    time_convert(time_lapsed)


def get_scan_results(image, margin, line, model):
    results = scan(image) if margin is None else scan(image, margin, model)
    return results.get_lines() if line is None else results.get_lines(line)


def time_convert(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    click.echo("Time Lapsed = {0}:{1}:{2}".format(int(hours), int(mins % 60), sec), err=True)


if __name__ == '__main__':
    ocr()
