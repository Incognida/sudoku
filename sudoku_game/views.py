from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import SudokuTable
from .sudoku_generator import generate_sudokus


class SudokuGenerateView(ListAPIView):
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        batch_solved = []
        batch_generated = []
        db_sudoku = []
        for _ in range(10):
            solved, generated = generate_sudokus()
            batch_solved.append(solved)
            batch_generated.append(generated)
            solved_db = SudokuTable(
                solved_table=solved
            )
            db_sudoku.append(solved_db)
        SudokuTable.objects.bulk_create(db_sudoku)
        sudokus = {
            "generated": batch_generated,
            "solved": batch_solved,
        }
        return Response(sudokus, status=201)


class SingleSudokuView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        solved, generated = generate_sudokus()
        sudoku = {
            "sudoku": generated
        }
        return Response(sudoku, status=201)
